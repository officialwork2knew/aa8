import streamlit as st
import json
from datetime import datetime
import os

DATA_FILE = "todos.json"

def load_todos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(DATA_FILE, "w") as f:
        json.dump(todos, f, indent=2)

if "todos" not in st.session_state:
    st.session_state.todos = load_todos()
st.title("📝 Todo App")

col1, col2 = st.columns([4, 1])
with col1:
    new_todo = st.text_input("Add new todo", key="new_todo_input")
with col2:
    st.write(""); st.write("")
    if st.button("Add", use_container_width=True):
        if new_todo.strip():
            todo = {
                "id": len(st.session_state.todos) + 1,
                "text": new_todo,
                "completed": False,
                "created": datetime.now().isoformat()
            }
            st.session_state.todos.append(todo)
            save_todos(st.session_state.todos)
            st.rerun()

st.divider()

filter_option = st.radio("Filter", ["All", "Active", "Completed"], horizontal=True)

filtered_todos = st.session_state.todos
if filter_option == "Active":
    filtered_todos = [t for t in st.session_state.todos if not t["completed"]]
elif filter_option == "Completed":
    filtered_todos = [t for t in st.session_state.todos if t["completed"]]

total = len(st.session_state.todos)
completed = len([t for t in st.session_state.todos if t["completed"]])
active = total - completed

col1, col2, col3 = st.columns(3)
col1.metric("Total", total)
col2.metric("Active", active)
col3.metric("Completed", completed)

st.divider()

if not filtered_todos:
    st.info("No todos yet!")
else:
    for idx, todo in enumerate(filtered_todos):
        col1, col2, col3 = st.columns([0.5, 4, 1])

        with col1:
            checked = st.checkbox("", value=todo["completed"], key=f"check_{todo['id']}")
            if checked != todo["completed"]:
                for t in st.session_state.todos:
                    if t["id"] == todo["id"]:
                        t["completed"] = checked
                save_todos(st.session_state.todos)
                st.rerun()

        with col2:
            if todo["completed"]:
                st.markdown(f"~~{todo['text']}~~")
            else:
                st.write(todo["text"])

        with col3:
            if st.button("🗑️", key=f"del_{todo['id']}", use_container_width=True):
                st.session_state.todos = [t for t in st.session_state.todos if t["id"] != todo["id"]]
                save_todos(st.session_state.todos)
                st.rerun()

st.divider()

if st.session_state.todos:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear Completed", use_container_width=True):
            st.session_state.todos = [t for t in st.session_state.todos if not t["completed"]]
            save_todos(st.session_state.todos)
            st.rerun()
    with col2:
        if st.button("Clear All", use_container_width=True, type="secondary"):
            st.session_state.todos = []
            save_todos(st.session_state.todos)
            st.rerun()
