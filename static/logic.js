
function editTask(taskId, taskText) {
    const taskTextElement = document.getElementById(`taskText_${taskId}`);

    // Check if the taskTextElement is already in edit mode
    if (taskTextElement.querySelector('input[type="text"]')) {
        return; // Do nothing if already in edit mode
    }

    // Create an input element to edit the task
    const inputElement = document.createElement('input');
    inputElement.setAttribute('type', 'text');
    inputElement.setAttribute('class', 'form-control');
    inputElement.value = taskText;

  //Create a "Save" button
const saveButton = document.createElement('button');
saveButton.textContent = 'Save'; // Set the button text
saveButton.addEventListener('click', () => {
    const updatedText = inputElement.value;
    sendUpdatedTaskToServer(taskId, updatedText)
        .then(response => {
            if (response.success) {
                taskTextElement.textContent = updatedText;
                inputElement.remove(); // Remove the input field
                saveButton.remove(); // Remove the "Save" button

                // Simulate a page reload by changing the URL
                window.location.href = window.location.href;
            } else {
                console.error('Failed to update task.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

    // Handle key press events for the input field (same as before)

    // Replace the task text with the input field and the "Save" button
    taskTextElement.textContent = '';
    taskTextElement.appendChild(inputElement);
    taskTextElement.appendChild(saveButton); // Append the "Save" button

    inputElement.focus(); // Focus on the input field
}





function sendUpdatedTaskToServer(taskId, updatedText) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const formData = new FormData();
    formData.append('task_id', taskId);
    formData.append('task', updatedText);

    return fetch(`/todos/editTask/${taskId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken,
        },
    })
    .then(response => response.json());
}



  function toggleTaskInput() {
      const taskInputContainer = document.getElementById('taskInputContainer');
      const formElement = document.createElement('form'); // Create a form element
      formElement.method = 'post'; // Set the form method
      formElement.action = "{% url 'addTask' %}"; // Set the form action

      const inputElement = document.createElement('input');
      inputElement.setAttribute('type', 'text');
      inputElement.setAttribute('class', 'form-control');
      inputElement.setAttribute('size', '100');
      inputElement.setAttribute('name', 'task'); // Set the input field name

      const submitButton = document.createElement('input'); // Create a submit button
      submitButton.setAttribute('type', 'submit'); // Set the button type to submit
      submitButton.setAttribute('value', 'Add'); // Set the button label

      // Add event listeners for Enter keypress events
      inputElement.addEventListener('keydown', function (e) {
          if (e.keyCode === 13) {
              e.preventDefault(); // Prevent form submission
              saveTaskToDatabase(inputElement.value);
              inputElement.value = ''; // Clear input after saving
              inputElement.focus(); // Focus on the input field
          }
      });

      // Add a submit event listener to the form
      formElement.addEventListener('submit', function (e) {
          e.preventDefault(); // Prevent the default form submission
          saveTaskToDatabase(inputElement.value);
          inputElement.value = ''; // Clear input after saving
          inputElement.focus(); // Focus on the input field
      });

      // Append the input field and submit button to the form
      formElement.appendChild(inputElement);
      formElement.appendChild(submitButton);

      // Clear existing content and then append the form element
      taskInputContainer.innerHTML = '';
      taskInputContainer.appendChild(formElement);

      inputElement.focus(); // Focus on the input field
      taskInputContainer.classList.toggle('d-none'); // Show the input container
  }

        
       // save task
function saveTaskToDatabase(taskText) {
    if (taskText.trim() === '') {
        return; // Don't save empty tasks
    }

    // Access the CSRF token from the global variable
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Send a POST request to the server using AJAX
    const formData = new FormData();
    formData.append('task', taskText);

    fetch('/todos/addTask/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken, // Use the CSRF token here
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Task saved successfully, you can take appropriate action
                window.location.reload(); // Reload the page to see the updated task list
            } else {
                console.error('Failed to save task.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
        document.addEventListener('DOMContentLoaded', function () {
            const completedToggle = document.getElementById('completedToggle'); // complete markdown 

            const completedTasksSection = document.getElementById('completedTasksSection'); // complete tasks section container 

            completedTasksSection.classList.add('d-none'); // Hide the completed tasks section initially


            completedToggle.addEventListener('click', function () {
                completedTasksSection.classList.toggle('d-none');

            });
        });

