<template>
  <div>
    <h1>Add item on list</h1>
    <form @submit.prevent="submitForm">
      <label for="text">Item Text:</label>
      <input type="text" id="text" v-model="text" required />
      <button type="submit">Create Item</button>
    </form>
    <p v-if="message">{{ message }}</p>
    <h2>List of created items:</h2>
    <ol id="list-all">
      <li class="list-item" v-for="item in items" :key="item.id">
        <div>ID: {{ item.id }} Text: {{ item.text }}</div>
        <button @click="deleteItem(item.id)" class="delete-btn">X</button>
      </li>
    </ol>

    <h1>Update by ID</h1>
    <form @submit.prevent="updateItem">
      <label for="update-id">Item ID:</label>
      <input type="number" id="update-id" v-model.number="updateId" required />
      <label for="update-text">New Text:</label>
      <input type="text" id="update-text" v-model="updateText" required />
      <button type="submit">Update Item</button>
    </form>
    <p v-if="updateMessage">{{ updateMessage }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const items = ref([]);
const text = ref("");
const message = ref("");

// Function to handle form submission
const submitForm = async () => {
  try {
    const formData = new FormData();
    formData.append("text", text.value);

    const response = await fetch("http://localhost:8000/items/create", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      message.value = `Item created: ${data.item.text} (ID: ${data.item.id})`;
      text.value = ""; // Clear the form input

      // Fetch items to update the list
      fetchItems();
    } else {
      message.value = `Error: ${response.statusText}`;
    }
  } catch (error) {
    console.error("Error creating item:", error);
    message.value = "Error creating item";
  }
};

// Function to handle form submission for updating an item
const updateId = ref(null);
const updateText = ref("");
const updateMessage = ref("");
const updateItem = async () => {
  try {
    const formData = new FormData();
    formData.append("text", updateText.value);

    const response = await fetch(
      `http://localhost:8000/items/editbyid/${updateId.value}`,
      {
        method: "PUT",
        body: formData,
      }
    );

    if (response.ok) {
      const data = await response.json();
      updateMessage.value = `Item updated: ${data.item.text} (ID: ${data.item.id})`;
      updateId.value = null; // Clear the ID input
      updateText.value = ""; // Clear the text input
      fetchItems(); // Refresh the list of items
    } else {
      updateMessage.value = `Error: ${response.statusText}`;
    }
  } catch (error) {
    console.error("Error updating item:", error);
    updateMessage.value = "Error updating item";
  }
};

// Function to fetch items from the server
const fetchItems = async () => {
  try {
    const response = await fetch("http://localhost:8000/items/findall");
    if (response.ok) {
      items.value = await response.json();
    } else {
      console.error("Failed to fetch items:", response.statusText);
    }
  } catch (error) {
    console.error("Error fetching items:", error);
  }
};

const deleteItem = async (id) => {
  try {
    const response = await fetch(`http://localhost:8000/items/deletebyid/${id}`, {
      method: "DELETE",
    });

    if (response.ok) {
      message.value = `Item with ID ${id} deleted.`;
      fetchItems(); // Refresh the list of items
    } else {
      message.value = `Error: ${response.statusText}`;
    }
  } catch (error) {
    console.error("Error deleting item:", error);
    message.value = "Error deleting item";
  }
};

// Fetch items when the component is mounted
onMounted(() => {
  fetchItems();
});
</script>

<style scoped>
#list-all {
  list-style-type: none;
  text-align: left;
  padding: 0 35%;
}

.list-item{
  display: flex;
  justify-content: space-between;
}

.delete-btn {
  background-color: red;
  color: white;
  border: none;
  padding: 4px 8px;
  cursor: pointer;
  border-radius: 4px;
}

.delete-btn:hover {
  background-color: darkred;
}
</style>
