# Food Suggestion 🍽️  

A web application that enables users to explore and review **Korean dishes and ingredients**. Built with Python Flask and Jinja2 templates, it offers personalized recommendations, user authentication via Google, and comprehensive filtering options.  

## 🌟 Features  

- 🔐 **User Authentication**: Secure login using Google accounts.  
- 🔍 **Search Functionality**: Find Korean dishes and ingredients with ease.  
- 🎯 **Personalized Recommendations**: Receive dish suggestions tailored to your taste preferences and dietary needs.  
- 📝 **Comprehensive Reviews**: Evaluate dishes based on dietary information and ingredient flavors; assess ingredients for their nutritional content.  
- ❤️ **Favorites Management**: Save and manage your preferred dishes and ingredients.  
- 🔄 **Advanced Filtering**:  
  - Sort dishes by taste profiles, dietary restrictions, and specific ingredients.  
  - Filter ingredients by nutritional values and associated dishes.  
- 👤 **User Profiles**: Access your review history and manage personal information.  
- ✏️ **Review Management**: Update or delete your past reviews as needed.  

## 🛠️ Tech Stack  

- **Backend**: Python Flask  
- **Frontend**: Jinja2 Templates  
- **Database**: Firebase  
- **Authentication**: Google Authentication
- **Deployment**: Render
- **Version Control**: Git
- **Uptime Monitoring**: Uptime Robot

## 🚀 Software Engineering Best Practices Followed

- **MVC Architecture**: Separates concerns into models, views, and controllers, making the code easier to maintain and extend.
- **Aggregate Pattern**: Efficiently handles complex review data, improving performance.
- **OOP (Object-Oriented Programming)**: Organizes the code with reusable classes, ensuring scalability and clarity.
- **Single Responsibility Principle**: Each function and class has a clear, single purpose, reducing complexity.
- **Separation of Concerns**: Keeps the different parts of the application independent (e.g., data handling, user interface), making debugging and updates easier.
- **Loose Coupling**: Reduces dependencies between components, allowing for simpler updates and changes.
- **Open/Closed Principle**: The app can be extended with new features without changing existing code.
- **DRY (Don't Repeat Yourself)**: Reduces redundant code by creating reusable functions and classes.
- **Security Best Practices**: Uses Google Sign-In for secure user authentication, and sensitive data like API keys are stored safely in environment variables.
- **Version Control**: Git and GitHub ensure code changes are well-managed and facilitate collaboration.
- **User-Centered Design**: Features like personalized recommendations and filtering are designed to provide a better user experience.
- **Scalable and Maintainable**: The code is structured to allow easy addition of features and future growth.

## 🚀 Live Demo  

🔗 [Food Suggestion](https://food-suggestion.onrender.com/)  

## 📦 Setup & Installation  

For developers interested in running the project locally:  

1. **Clone the repository**:  
   ```sh
   git clone https://github.com/lucakim27/food-suggestion.git
   cd food-suggestion
   ```

2. **Set up a virtual environment**:
    ```sh
    python3 -m venv venv
    source .venv/bin/activate
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Configure environment variables**:
    - Create a .env file in the root directory.
    - Add your Firebase and Google Sign-In credentials to the .env file.

5. **Start the Flask server**:
    ```sh
    flask run
    ```

6. **Access the application**:
    - Navigate to http://127.0.0.1:5000 in your web browser.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements or bug fixes.

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.