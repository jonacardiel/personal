#include <iostream>    // Required for input/output operations (cin, cout)
#include <vector>      // Required for std::vector, an STL data structure
#include <string>      // Required for std::string
#include <limits>      // Required for numeric_limits to clear input buffer
#include <fstream>     // Required for file stream operations (ifstream, ofstream)
#include <iomanip>     // Required for std::fixed and std::setprecision for output formatting

// --- 1. Class Definition ---
// The Student class encapsulates data and behavior related to a single student.
class Student {
public:
    // Attributes (data members) of the Student class
    std::string name;
    int id;
    std::vector<double> grades; // STL data structure: std::vector to store grades

    // Constructor: A special function called when a Student object is created.
    // It initializes the object's attributes.
    Student(std::string name, int id) : name(name), id(id) {}

    // Member function to add a grade to the student's record.
    void addGrade(double grade) {
        grades.push_back(grade);
    }

    // Member function to calculate the average grade for the student.
    // Demonstrates a loop and a conditional.
    double calculateAverage() const {
        if (grades.empty()) { // Conditional: Check if there are no grades
            return 0.0;       // Return 0 if no grades to avoid division by zero
        }
        double sum = 0.0;
        // Loop: Iterate through all grades in the vector
        for (double grade : grades) {
            sum += grade;
        }
        return sum / grades.size();
    }

    // Member function to display student details.
    // Demonstrates output formatting.
    void displayStudentInfo() const {
        std::cout << "  ID: " << id << ", Name: " << name;
        std::cout << ", Average Grade: " << std::fixed << std::setprecision(2) << calculateAverage();
        std::cout << ", Grades: [";
        // Loop: Iterate through grades to display them
        for (size_t i = 0; i < grades.size(); ++i) {
            std::cout << grades[i];
            if (i < grades.size() - 1) {
                std::cout << ", ";
            }
        }
        std::cout << "]" << std::endl;
    }
};

// --- Global Vector to store all students ---
// This vector will hold all the Student objects in our system.
std::vector<Student> students;

// --- 2. Functions for managing students ---

// Function to clear the input buffer after reading numbers.
// Prevents issues with subsequent getline() calls.
void clearInputBuffer() {
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

// Function to add a new student to the system.
// Demonstrates input and adding to an STL vector.
void addStudent() {
    std::string name;
    int id;

    std::cout << "\n--- Add New Student ---" << std::endl;
    std::cout << "Enter student name: ";
    std::cin.ignore(); // Clear the buffer before reading string with spaces
    std::getline(std::cin, name);

    std::cout << "Enter student ID: ";
    // Loop and Conditional: Input validation loop to ensure ID is a number
    while (!(std::cin >> id)) {
        std::cout << "Invalid ID. Please enter a number: ";
        std::cin.clear(); // Clear error flags
        clearInputBuffer(); // Discard invalid input
    }
    clearInputBuffer(); // Clear buffer after reading ID

    // Conditional: Check if a student with this ID already exists
    bool idExists = false;
    for (const auto& student : students) {
        if (student.id == id) {
            idExists = true;
            break;
        }
    }

    if (idExists) {
        std::cout << "Error: Student with ID " << id << " already exists." << std::endl;
    } else {
        students.emplace_back(name, id); // Create a new Student object and add to vector
        std::cout << "Student '" << name << "' (ID: " << id << ") added successfully." << std::endl;
    }
}

// Function to add a grade for an existing student.
// Demonstrates searching using a loop and updating an object's state.
void addGrade() {
    int id;
    double grade;

    std::cout << "\n--- Add Grade ---" << std::endl;
    std::cout << "Enter student ID to add grade for: ";
    while (!(std::cin >> id)) {
        std::cout << "Invalid ID. Please enter a number: ";
        std::cin.clear();
        clearInputBuffer();
    }

    // Loop: Iterate through students to find the matching ID
    // Conditional: Check if student is found
    Student* foundStudent = nullptr; // Pointer to found student
    for (Student& s : students) { // Use reference to modify the actual student object
        if (s.id == id) {
            foundStudent = &s;
            break;
        }
    }

    if (foundStudent) {
        std::cout << "Enter grade for " << foundStudent->name << ": ";
        while (!(std::cin >> grade) || grade < 0 || grade > 100) { // Conditional: Validate grade range
            std::cout << "Invalid grade. Please enter a number between 0 and 100: ";
            std::cin.clear();
            clearInputBuffer();
        }
        foundStudent->addGrade(grade); // Call member function to add grade
        std::cout << "Grade " << grade << " added for " << foundStudent->name << "." << std::endl;
    } else {
        std::cout << "Student with ID " << id << " not found." << std::endl;
    }
    clearInputBuffer(); // Clear buffer after reading grade
}

// Function to display information for all students.
// Demonstrates iterating through the STL vector.
void listAllStudents() {
    std::cout << "\n--- All Students ---" << std::endl;
    if (students.empty()) { // Conditional: Check if no students exist
        std::cout << "No students registered yet." << std::endl;
        return;
    }
    // Loop: Iterate through each student in the vector and display their info
    for (const auto& student : students) {
        student.displayStudentInfo(); // Call member function to display info
    }
}

// --- Stretch Challenge: File I/O ---

// Function to save student data to a file.
// Demonstrates writing to a file.
void saveStudentsToFile(const std::string& filename) {
    std::ofstream outFile(filename); // Create an output file stream

    if (!outFile.is_open()) { // Conditional: Check if file opened successfully
        std::cerr << "Error: Could not open file " << filename << " for writing." << std::endl;
        return;
    }

    // Loop: Iterate through each student and write their data
    for (const auto& student : students) {
        outFile << student.name << "," << student.id;
        // Loop: Write each grade, separated by commas
        for (double grade : student.grades) {
            outFile << "," << grade;
        }
        outFile << "\n"; // Newline after each student's data
    }

    outFile.close(); // Close the file
    std::cout << "Student data saved to " << filename << std::endl;
}

// Function to load student data from a file.
// Demonstrates reading from a file and parsing data.
void loadStudentsFromFile(const std::string& filename) {
    std::ifstream inFile(filename); // Create an input file stream

    if (!inFile.is_open()) { // Conditional: Check if file opened successfully
        std::cerr << "Error: Could not open file " << filename << " for reading." << std::endl;
        return;
    }

    students.clear(); // Clear existing student data before loading new data

    std::string line;
    // Loop: Read file line by line
    while (std::getline(inFile, line)) {
        std::string name;
        int id;
        std::vector<double> currentGrades;
        std::string segment;
        size_t start = 0;
        size_t end = line.find(','); // Find first comma

        // Extract name
        if (end != std::string::npos) {
            name = line.substr(start, end - start);
            start = end + 1;
            end = line.find(',', start); // Find second comma
        } else {
            // Handle case where only name might be present (unlikely with ID)
            name = line.substr(start);
            // If no ID or grades, skip this line or handle as error
            continue;
        }

        // Extract ID
        if (end != std::string::npos) {
            id = std::stoi(line.substr(start, end - start));
            start = end + 1;
        } else {
            // If only name and ID, no grades
            id = std::stoi(line.substr(start));
            students.emplace_back(name, id);
            continue; // Move to next line
        }

        // Extract grades (loop through remaining segments)
        while (start < line.length()) {
            end = line.find(',', start);
            segment = line.substr(start, (end == std::string::npos) ? std::string::npos : end - start);
            try {
                currentGrades.push_back(std::stod(segment)); // Convert string to double
            } catch (const std::invalid_argument& e) {
                std::cerr << "Warning: Invalid grade format in line: " << line << std::endl;
            } catch (const std::out_of_range& e) {
                std::cerr << "Warning: Grade out of range in line: " << line << std::endl;
            }
            if (end == std::string::npos) {
                break; // No more commas, end of line
            }
            start = end + 1;
        }

        Student newStudent(name, id);
        for (double grade : currentGrades) {
            newStudent.addGrade(grade);
        }
        students.push_back(newStudent);
    }

    inFile.close(); // Close the file
    std::cout << "Student data loaded from " << filename << std::endl;
}

// Function to edit or update a specific grade for a student.
void editGrade() {
    int id;
    std::cout << "\n--- Edit Student Grade ---" << std::endl;
    std::cout << "Enter student ID: ";
    while (!(std::cin >> id)) {
        std::cout << "Invalid ID. Please enter a number: ";
        std::cin.clear();
        clearInputBuffer();
    }

    Student* foundStudent = nullptr;
    for (Student& s : students) {
        if (s.id == id) {
            foundStudent = &s;
            break;
        }
    }

    if (!foundStudent) {
        std::cout << "Student with ID " << id << " not found." << std::endl;
        clearInputBuffer();
        return;
    }

    if (foundStudent->grades.empty()) {
        std::cout << "No grades to edit for this student." << std::endl;
        clearInputBuffer();
        return;
    }

    std::cout << "Grades for " << foundStudent->name << ": ";
    for (size_t i = 0; i < foundStudent->grades.size(); ++i) {
        std::cout << "[" << i << "] " << foundStudent->grades[i];
        if (i < foundStudent->grades.size() - 1) std::cout << ", ";
    }
    std::cout << std::endl;

    size_t gradeIndex;
    std::cout << "Enter the index of the grade to edit (0-" << foundStudent->grades.size() - 1 << "): ";
    while (!(std::cin >> gradeIndex) || gradeIndex >= foundStudent->grades.size()) {
        std::cout << "Invalid index. Please enter a valid grade index: ";
        std::cin.clear();
        clearInputBuffer();
    }

    double newGrade;
    std::cout << "Enter new grade (0-100): ";
    while (!(std::cin >> newGrade) || newGrade < 0 || newGrade > 100) {
        std::cout << "Invalid grade. Please enter a number between 0 and 100: ";
        std::cin.clear();
        clearInputBuffer();
    }

    foundStudent->grades[gradeIndex] = newGrade;
    std::cout << "Grade updated successfully." << std::endl;
    clearInputBuffer();
}

// --- Main Program Loop ---
// The entry point of the program.
int main() {
    std::string filename = "students.txt"; // Default filename for saving/loading

    // Conditional: Offer to load data at startup
    char choice;
    std::cout << "Do you want to load student data from '" << filename << "'? (y/n): ";
    std::cin >> choice;
    if (tolower(choice) == 'y') {
        loadStudentsFromFile(filename);
    }
    clearInputBuffer(); // Clear buffer after reading choice

    int option;
    // Loop: Main menu loop, continues until user chooses to exit
    do {
        std::cout << "\n--- Student Management System Menu ---" << std::endl;
        std::cout << "1. Add New Student" << std::endl;
        std::cout << "2. Add Grade for Student" << std::endl;
        std::cout << "3. List All Students" << std::endl;
        std::cout << "4. Save Data to File" << std::endl;
        std::cout << "5. Load Data from File" << std::endl;
        std::cout << "6. Edit Student Grade" << std::endl;
        std::cout << "7. Exit" << std::endl;
        std::cout << "Enter your choice: ";

        // Conditional and Loop: Input validation for menu option
        while (!(std::cin >> option) || option < 1 || option > 7) {
            std::cout << "Invalid option. Please enter a number between 1 and 7: ";
            std::cin.clear();
            clearInputBuffer();
        }

        // Conditional (Switch-case): Perform action based on user's choice
        switch (option) {
            case 1:
                addStudent();
                break;
            case 2:
                addGrade();
                break;
            case 3:
                listAllStudents();
                break;
            case 4:
                saveStudentsToFile(filename);
                break;
            case 5:
                loadStudentsFromFile(filename);
                break;
            case 6:
                editGrade();
                break;
            case 7:
                std::cout << "Exiting program. Goodbye!" << std::endl;
                break;
            default:
                // This case should ideally not be reached due to input validation
                std::cout << "An unexpected error occurred." << std::endl;
                break;
        }
    } while (option != 7); // Loop condition: Continue until option 7 is chosen

    return 0; // Indicate successful program execution
}
