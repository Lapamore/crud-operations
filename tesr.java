import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.CountDownLatch;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class ThirdLab {

    private static final Pattern TYPE_DECL_PATTERN = Pattern.compile(
            "(?m)(?:^|\\s)(?:public|protected|private|abstract|final|static|sealed|non-sealed|strictfp)?\\s*" +
            "(class|interface)\\s+([A-Za-z_][\\w$]*)\\s*" +
            "(?:extends\\s+([A-Za-z_][\\w$]*(?:\\s*,\\s*[A-Za-z_][\\w$]*)*))?\\s*" +
            "(?:implements\\s+([A-Za-z_][\\w$]*(?:\\s*,\\s*[A-Za-z_][\\w$]*)*))?"
    );

    public static void main(String[] args) {

        Path root = Paths.get(args[0]).toAbsolutePath().normalize();
        if (!Files.exists(root) || !Files.isDirectory(root)) {
            System.err.println("Путь не существует или не является директорией: " + root);
            System.exit(2);
        }

        Map<String, Set<String>> parentToChildren = new HashMap<>();
        Set<String> allTypes = new HashSet<>();

        try (Stream<Path> paths = Files.walk(root)) {
            List<Path> javaFiles = paths
                    .filter(p -> Files.isRegularFile(p) && p.toString().endsWith(".java"))
                    .collect(Collectors.toList());

            System.out.println("Найдено файлов .java: " + javaFiles.size());

            CountDownLatch latch = new CountDownLatch(javaFiles.size());

            List<Map<String, Set<String>>> threadParentToChildrenResults = Collections.synchronizedList(new ArrayList<>());
            List<Set<String>> threadAllTypesResults = Collections.synchronizedList(new ArrayList<>());

            for (Path file : javaFiles) {
                Thread t = new Thread(() -> {
                    try {
                        String source = readFile(file);

                        Map<String, Set<String>> localParentToChildren = new HashMap<>();
                        Set<String> localAllTypes = new HashSet<>();

                        Matcher m = TYPE_DECL_PATTERN.matcher(source);
                        while (m.find()) {
                            String typeName = m.group(2);
                            String extendsPart = m.group(3);
                            String implementsPart = m.group(4);

                            localAllTypes.add(typeName);

                            if (extendsPart != null && !extendsPart.isBlank()) {
                                for (String parent : splitByComma(extendsPart)) {
                                    addEdge(localParentToChildren, parent.trim(), typeName);
                                }
                            }

                            if (implementsPart != null && !implementsPart.isBlank()) {
                                for (String parent : splitByComma(implementsPart)) {
                                    addEdge(localParentToChildren, parent.trim(), typeName);
                                }
                            }
                        }

                        threadParentToChildrenResults.add(localParentToChildren);
                        threadAllTypesResults.add(localAllTypes);

                    } catch (IOException e) {
                        System.err.println("Ошибка ввода-вывода в потоке при обработке " + file + ": " + e.getMessage());
                    } finally {
                        latch.countDown();
                    }
                });

                t.start();
            }

            try {
                latch.await();
            } catch (InterruptedException e) {
                System.err.println("Основной поток прерван во время ожидания рабочих: " + e.getMessage());
                Thread.currentThread().interrupt();
                System.exit(4);
            }

            System.out.println("Все потоки завершены. Начинается объединение результатов...");

            for (Map<String, Set<String>> localMap : threadParentToChildrenResults) {
                for (Map.Entry<String, Set<String>> entry : localMap.entrySet()) {
                    String parent = entry.getKey();
                    Set<String> children = entry.getValue();
                    Set<String> globalChildren = parentToChildren.computeIfAbsent(parent, k -> new TreeSet<>());
                    globalChildren.addAll(children);
                }
            }

            for (Set<String> localSet : threadAllTypesResults) {
                allTypes.addAll(localSet);
            }

            for (String t : allTypes) {
                parentToChildren.putIfAbsent(t, new TreeSet<>());
            }

            System.out.println("\n--- Статистика ---");
            System.out.println("Всего уникальных типов: " + allTypes.size());
            System.out.println("Всего типов с потомками: " + (int) parentToChildren.entrySet().stream().filter(e -> !e.getValue().isEmpty()).count());
            System.out.println("Всего потомков: " + parentToChildren.values().stream().mapToInt(Set::size).sum());
            System.out.println("------------------\n");

            parentToChildren.entrySet().stream()
                    .sorted(Map.Entry.comparingByKey())
                    .forEach(entry -> {
                        String parent = entry.getKey();
                        Set<String> children = new TreeSet<>(parentToChildren.getOrDefault(parent, Collections.emptySet()));
                        System.out.println(parent + " -> " +
                                (children.isEmpty()
                                        ? "[]"
                                        : children.stream().collect(Collectors.joining(", ", "[", "]"))));
                    });

        } catch (IOException e) {
            System.err.println("Ошибка ввода-вывода: " + e.getMessage());
            System.exit(3);
        }
    }

    private static void addEdge(Map<String, Set<String>> parentToChildren, String parent, String child) {
        Set<String> set = parentToChildren.computeIfAbsent(parent, k -> new TreeSet<>());
        set.add(child);
    }

    private static List<String> splitByComma(String s) {
        return Arrays.stream(s.split(","))
                .map(String::trim)
                .filter(t -> !t.isEmpty())
                .collect(Collectors.toList());
    }

    private static String readFile(Path p) throws IOException {
        byte[] bytes = Files.readAllBytes(p);
        return new String(bytes, StandardCharsets.UTF_8);
    }
}