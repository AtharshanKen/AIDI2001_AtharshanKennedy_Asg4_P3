import pytest
from streamlit.testing.v1 import AppTest

def test_initial_app_elements():
    at = AppTest.from_file("app.py")
    at.run()

    # Check for title input field
    assert at.text_input[0].label_visibility == "hidden"
    assert at.text_input[0].value == ""

    # Check for description input field
    assert at.text_input[1].label_visibility == "hidden"
    assert at.text_input[1].value == ""

    # Check for 'Add Task' button
    assert at.button[0].label == "Add Task"

def test_add_task():
    at = AppTest.from_file("app.py")
    at.run()

    # Simulate user input
    at.text_input[0].set_value("Test Title").run()
    at.text_input[1].set_value("Test Description").run()

    # Click the 'Add Task' button
    at.button[0].click().run()

    # Assert that the task is added to session state
    assert len(at.session_state.tasks) == 1
    assert at.session_state.tasks[0]["title"] == "Test Title"
    assert at.session_state.tasks[0]["description"] == "Test Description"

    # Also check that input fields are cleared after submission
    assert at.text_input[0].value == ""
    assert at.text_input[1].value == ""

def test_display_tasks_with_remove_button():
    at = AppTest.from_file("app.py")
    at.run()

    # Add a task
    at.text_input[0].set_value("Task to Display").run()
    at.text_input[1].set_value("Description of task to display").run()
    at.button[0].click().run()

    # Re-run the app to update the display
    at.run()

    # Assert that the task is in session state
    assert len(at.session_state.tasks) == 1
    assert at.session_state.tasks[0]["title"] == "Task to Display"

    # Assert that the task title and description are visible in the rendered output
    found_task_display = False
    for markdown_element in at.markdown:
        if "Task to Display" in markdown_element.value and "Description of task to display" in markdown_element.value:
            found_task_display = True
            break
    assert found_task_display, "Task title and description not found in rendered markdown."

    # Assert that at least one 'Remove' button exists (beyond the initial 'Add Task' button)
    # We need to count buttons after the 'Add Task' button, which is at index 0.
    # The remove buttons start from index 1 in at.button list
    assert len(at.button) > 1, "Expected a 'Remove' button to be present for the displayed task."

def test_remove_task():
    at = AppTest.from_file("app.py")
    at.run()

    # Add two tasks
    at.text_input[0].set_value("First Task").run()
    at.text_input[1].set_value("Description 1").run()
    at.button[0].click().run()

    at.text_input[0].set_value("Second Task").run()
    at.text_input[1].set_value("Description 2").run()
    at.button[0].click().run()

    at.run() # Re-run to update the display with remove buttons

    assert len(at.session_state.tasks) == 2

    # Click the 'Remove' button for the first task (index 0, which corresponds to button[1])
    # The 'Add Task' button is button[0], subsequent buttons are 'Remove' buttons.
    # We need to find the correct button by its key, or assume order.
    # Let's target the button for the first task. Streamlit's testing API orders buttons by appearance.
    # The first remove button will be at index 1.
    remove_button_for_first_task_found = False
    for btn in at.button:
        if btn.label == "Remove" and btn.key == "remove_task_0":
            btn.click().run()
            remove_button_for_first_task_found = True
            break

    assert remove_button_for_first_task_found, "Could not find and click remove button for first task."

    # Assert that one task has been removed from session state
    assert len(at.session_state.tasks) == 1
    # Assert that the remaining task is the second one
    assert at.session_state.tasks[0]["title"] == "Second Task"

    # Re-run the app again to ensure the display updates correctly
    at.run()

    # Assert that the first task's title is no longer in the rendered output
    found_first_task_title = False
    for markdown_element in at.markdown:
        if "First Task" in markdown_element.value:
            found_first_task_title = True
            break
    assert not found_first_task_title, "First Task title should not be in rendered markdown after removal."

    # Assert that the second task's title is still in the rendered output
    found_second_task_title = False
    for markdown_element in at.markdown:
        if "Second Task" in markdown_element.value:
            found_second_task_title = True
            break
    assert found_second_task_title, "Second Task title should still be in rendered markdown after removal."
