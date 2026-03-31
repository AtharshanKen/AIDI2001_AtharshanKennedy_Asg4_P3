import streamlit as st

st.set_page_config(layout="wide")
st.title("My To-Do App")

# Initialize tasks in session state if not present
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Function to add a task
def add_new_task():
    if st.session_state.task_title_input and st.session_state.task_description_input:
        new_task = {
            "title": st.session_state.task_title_input,
            "description": st.session_state.task_description_input
        }
        st.session_state.tasks.append(new_task)
        st.session_state.task_title_input = ""  # Clear input
        st.session_state.task_description_input = "" # Clear input

# Function to remove a task
def remove_task(task_index):
    if task_index < len(st.session_state.tasks):
        st.session_state.tasks.pop(task_index)

# Task Input Section
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.text_input("Title", key="task_title_input", label_visibility="hidden", value="")
        st.text_input("Description", key="task_description_input", label_visibility="hidden", value="")
    with col2:
        st.button("Add Task", on_click=add_new_task)

# Task List Display Section
st.subheader("Current Tasks")
if not st.session_state.tasks:
    st.info("No tasks added yet!")
else:
    for i, task in enumerate(st.session_state.tasks):
        task_col, remove_col = st.columns([3, 1])
        with task_col:
            st.markdown(f"**{task['title']}**: {task['description']}")
        with remove_col:
            st.button("Remove", key=f"remove_task_{i}", on_click=remove_task, args=(i,))
