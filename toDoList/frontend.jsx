import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [todoList, setTodoList] = useState([]);
  const [taskList, setTaskList] = useState([]);
  const [newTodoListTitle, setNewTodoListTitle] = useState('');
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [selectedListId, setSelectedListId] = useState(null);
  const [authToken, setAuthToken] = useState(localStorage.getItem('authToken') || '');
  const [errorMessage, setErrorMessage] = useState(null);

  useEffect(() => {
    fetchTodoList();
  }, []);

  const handleLogin = async (username, password) => {
    try {
      const response = await fetch('/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ identifier: username, password })
      });
      const data = await response.json();
      if (data.success) {
        setAuthToken(data.success.split(' ')[1]); // Extract token from success message
        localStorage.setItem('authToken', data.success.split(' ')[1]);
        fetchTodoList();
      } else {
        setErrorMessage(data.error);
      }
    } catch (error) {
      console.error("Error logging in:", error);
      setErrorMessage("An error occurred. Please try again.");
    }
  };

  const fetchTodoList = async () => {
    try {
      const response = await fetch('/todo_list', {
        headers: {
          'Authorization': `Bearer ${authToken}`,
        }
      });
      const data = await response.json();
      setTodoList(data.todo_list || []);
      setErrorMessage(null); // Clear any previous errors
    } catch (error) {
      console.error("Error fetching to-do list:", error);
      setErrorMessage("An error occurred. Please try again.");
    }
  };

  const createTodoList = async (e) => {
    e.preventDefault();
    if (!authToken) {
      setErrorMessage("Please login to create lists.");
      return;
    }
    try {
      const response = await fetch('/todo_list', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title: newTodoListTitle })
      });
      const data = await response.json();
      console.log("To-Do List created successfully:", data);
      setNewTodoListTitle('');
      fetchTodoList();
    } catch (error) {
      console.error("Error creating to-do list:", error);
      setErrorMessage("An error occurred. Please try again.");
    }
  };

  const handleListSelect = (listId) => {
    setSelectedListId(listId);
    fetchTasks(listId);
  };

  const fetchTasks = async (listId) => {
    try {
      const response = await fetch(`/task?list_id=${listId}`, {
        headers: {
          'Authorization': `Bearer ${authToken}`,
        }
      });
      const data = await response.json();
      setTaskList(data.tasks || []);
      setErrorMessage(null); // Clear any previous errors
    } catch (error) {
      console.error("Error fetching tasks:", error);
      setErrorMessage("An error occurred. Please try again.");
    }
  };

  const createTask = async (e) => {
    e.preventDefault();
    if (!selectedListId || !authToken) return;
    try {
      const response = await fetch('/task', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ list_id: selectedListId, task_title: newTaskTitle })
      });
      const data = await response.json();
      console.log("Task created successfully:", data);
      setNewTaskTitle('');
      fetchTasks(selectedListId);
    } catch (error) {
      console.error("Error creating task:", error);
      setErrorMessage("An error occurred. Please try again.");
    }
    }
    
