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
        Set<String> allTypes = new HashSet<>(); // Теперь снова нужен глобальный Set для всех типов

        try (Stream<Path> paths = Files.walk(root)) {
            List<Path> javaFiles = paths
                    .filter(p -> Files.isRegularFile(p) && p.toString().endsWith(".java"))
                    .collect(Collectors.toList());

            System.out.println("Найдено файлов .java: " + javaFiles.size());

            CountDownLatch latch = new CountDownLatch(javaFiles.size());

            // Синхронизированный список для сбора результатов всех потоков
            List<Map<String, Set<String>>> threadParentToChildrenResults = Collections.synchronizedList(new ArrayList<>());
            // Синхронизированный список для сбора всех типов из всех потоков
            List<Set<String>> threadAllTypesResults = Collections.synchronizedList(new ArrayList<>());

            for (Path file : javaFiles) {
                Thread t = new Thread(() -> {
                    try {
                        String source = readFile(file);

                        // Локальные структуры данных для текущего потока
                        Map<String, Set<String>> localParentToChildren = new HashMap<>();
                        Set<String> localAllTypes = new HashSet<>(); // Один локальный Set для всех типов в файле

                        Matcher m = TYPE_DECL_PATTERN.matcher(source);
                        while (m.find()) {
                            String typeName = m.group(2); // Имя текущего типа (родителя или потомка)
                            String extendsPart = m.group(3); // может быть null
                            String implementsPart = m.group(4); // может быть null

                            // Добавляем текущий тип в локальный Set всех типов
                            localAllTypes.add(typeName);

                            // Обрабатываем extends
                            if (extendsPart != null && !extendsPart.isBlank()) {
                                for (String parent : splitByComma(extendsPart)) {
                                    // Добавляем родителя в локальный Set всех типов
                                    localAllTypes.add(parent.trim());
                                    // Добавляем связь: родитель -> текущий тип
                                    addEdge(localParentToChildren, parent.trim(), typeName);
                                }
                            }

                            // Обрабатываем implements
                            if (implementsPart != null && !implementsPart.isBlank()) {
                                for (String parent : splitByComma(implementsPart)) {
                                    // Добавляем родителя (интерфейс) в локальный Set всех типов
                                    localAllTypes.add(parent.trim());
                                    // Добавляем связь: родитель -> текущий тип
                                    addEdge(localParentToChildren, parent.trim(), typeName);
                                }
                            }
                        }

                        // Синхронизированно добавляем результаты потока в глобальные списки
                        threadParentToChildrenResults.add(localParentToChildren);
                        threadAllTypesResults.add(localAllTypes);

                    } catch (IOException e) {
                        System.err.println("Ошибка ввода-вывода в потоке при обработке " + file + ": " + e.getMessage());
                    } finally {
                        // Сообщаем защелке, что один поток завершил работу
                        latch.countDown();
                    }
                });

                t.start();
            }

            // Ждем завершения всех потоков
            try {
                latch.await();
            } catch (InterruptedException e) {
                System.err.println("Основной поток прерван во время ожидания рабочих: " + e.getMessage());
                Thread.currentThread().interrupt(); // Восстанавливаем статус прерывания
                System.exit(4);
            }

            System.out.println("Все потоки завершены. Начинается объединение результатов...");

            // Объединяем результаты всех потоков для parentToChildren
            for (Map<String, Set<String>> localMap : threadParentToChildrenResults) {
                for (Map.Entry<String, Set<String>> entry : localMap.entrySet()) {
                    String parent = entry.getKey();
                    Set<String> children = entry.getValue();
                    Set<String> globalChildren = parentToChildren.computeIfAbsent(parent, k -> new TreeSet<>());
                    globalChildren.addAll(children);
                }
            }

            // Объединяем результаты всех потоков для allTypes
            for (Set<String> localSet : threadAllTypesResults) {
                allTypes.addAll(localSet); // Объединяем все локальные Set в один глобальный
            }

            // Гарантируем, что каждый объявленный тип присутствует в карте (даже без потомков)
            for (String t : allTypes) {
                parentToChildren.putIfAbsent(t, new TreeSet<>());
            }

            System.out.println("\n--- Статистика ---");
            System.out.println("Всего уникальных типов: " + allTypes.size());
            System.out.println("Всего типов с потомками: " + (int) parentToChildren.entrySet().stream().filter(e -> !e.getValue().isEmpty()).count());
            System.out.println("Всего потомков: " + parentToChildren.values().stream().mapToInt(Set::size).sum());
            System.out.println("------------------\n");

            // Красивый вывод: типы по алфавиту, потомки по алфавиту
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

    // Построение связей между родителем и потомком
    private static void addEdge(Map<String, Set<String>> parentToChildren, String parent, String child) {
        Set<String> set = parentToChildren.computeIfAbsent(parent, k -> new TreeSet<>());
        set.add(child);
    }

    // Проверка случая если у нас через запятую несколько потомков extends или implements
    private static List<String> splitByComma(String s) {
        return Arrays.stream(s.split(","))
                .map(String::trim)
                .filter(t -> !t.isEmpty())
                .collect(Collectors.toList());
    }

    // Работа с файлами и кодировка его в байты
    private static String readFile(Path p) throws IOException {
        byte[] bytes = Files.readAllBytes(p);
        return new String(bytes, StandardCharsets.UTF_8);
    }
}