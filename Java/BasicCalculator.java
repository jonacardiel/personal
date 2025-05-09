import java.util.Scanner;

public class BasicCalculator {
    public static void main(String[] args) {
        double num1, num2;
        char operation;
        boolean running = true;
        double result = 0; // Declare the result variable

        System.out.println("Simple Command-Line Calculator");

        try (Scanner input = new Scanner(System.in)) {
            while (running) {
                // Removed unused variable 'result'
            System.out.println("\nEnter an operation (+, -, *, /, or 'q' to quit): ");
            operation = input.next().charAt(0);

            if (operation == 'q' || operation == 'Q') {
                running = false;
                System.out.println("Exiting calculator. Goodbye!");
                continue;
            }

            System.out.print("Enter first number: ");
            if (!input.hasNextDouble()) {
                System.out.println("Invalid input. Please enter a number.");
                input.next(); // Consume the invalid input
                continue;
            }
            num1 = input.nextDouble();

            System.out.print("Enter second number: ");
            if (!input.hasNextDouble()) {
                System.out.println("Invalid input. Please enter a number.");
                input.next(); // Consume the invalid input
                continue;
            }
            num2 = input.nextDouble();

            result = switch (operation) {
                case '+' -> {
                    double sum = num1 + num2;
                    System.out.println(num1 + " + " + num2 + " = " + sum);
                    yield sum;
                }
                case '-' -> {
                    double difference = num1 - num2;
                    System.out.println(num1 + " - " + num2 + " = " + difference);
                    yield difference;
                }
                case '*' -> {
                    double product = num1 * num2;
                    System.out.println(num1 + " * " + num2 + " = " + product);
                    yield product;
                }
                case '/' -> {
                    if (num2 != 0) {
                        double quotient = num1 / num2;
                        System.out.println(num1 + " / " + num2 + " = " + quotient);
                        yield quotient;
                    } else {
                        System.out.println("Error! Division by zero is not allowed.");
                        yield Double.NaN;
                    }
                }
                default -> {
                    System.out.println("Invalid operation!");
                    yield Double.NaN;
                }
            };
        }
        }
    }
}