import os
import csv
import json

class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")
        if os.path.exists(self.filename):
            print(f"File found: {self.filename}")
            return True
        else:
            print(f"File not found: {self.filename}")
            return False

    def create_output_folder(self, folder='output'):
        print("\nChecking output folder...")
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Output folder created: {folder}/")
        else:
            print(f"Output folder already exists: {folder}/")


class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("\nLoading data...")
        try:
            with open(self.filename, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.students = [row for row in reader]
            print(f"Data loaded successfully: {len(self.students)} students")
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
        return self.students

    def preview(self, n=5):
        print(f"\nFirst {n} rows:")
        print("-" * 30)
        for row in self.students[:n]:
            print(f"{row['student_id']} | {row['age']} | {row['gender']} | {row['country']} | GPA: {row['GPA']}")
        print("-" * 30)


class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        gpas = [float(student['GPA']) for student in self.students]

        avg_gpa = round(sum(gpas) / len(gpas), 2)
        max_gpa = max(gpas)
        min_gpa = min(gpas)
        high_performers = sum(1 for g in gpas if g > 3.5)

        self.result = {
            'total_students': len(self.students),
            'avg_gpa': avg_gpa,
            'max_gpa': max_gpa,
            'min_gpa': min_gpa,
            'high_performers': high_performers
        }
        return self.result

    def print_results(self):
        print("-" * 30)
        print("GPA Analysis")
        print("-" * 30)
        print(f"Total students : {self.result['total_students']}")
        print(f"Average GPA : {self.result['avg_gpa']}")
        print(f"Highest GPA : {self.result['max_gpa']}")
        print(f"Lowest GPA : {self.result['min_gpa']}")
        print(f"Students GPA > 3.5 : {self.result['high_performers']}")
        print("-" * 30)

class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(self.result, f, indent=4)
            print(f"Result saved to {self.output_path}")
        except Exception as e:
            print(f"Error saving file: {e}")


#Main
fm = FileManager('students.csv')
if not fm.check_file():
    print('Stopping program.')
    exit()
fm.create_output_folder()

dl = DataLoader('students.csv')
dl.load()
dl.preview()

analyser = DataAnalyser(dl.students)
analyser.analyse()
analyser.print_results()

saver = ResultSaver(analyser.result, 'output/result.json')
saver.save_json()