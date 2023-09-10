

    
        document.addEventListener('DOMContentLoaded', function () {
            const completedToggle = document.getElementById('completedToggle'); // complete markdown 

            const completedTasksSection = document.getElementById('completedTasksSection'); // complete tasks section container 

            completedTasksSection.classList.add('d-none'); // Hide the completed tasks section initially


            completedToggle.addEventListener('click', function () {
                completedTasksSection.classList.toggle('d-none');

            });
        });

