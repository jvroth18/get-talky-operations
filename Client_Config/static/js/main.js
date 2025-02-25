// main.js

// API Base URL
const API_BASE_URL = ''; // Adjust if needed, e.g. '/api'

// Utility function to show notifications
function showNotification(message, isError = false) {
  const notification = document.getElementById('notification');
  notification.textContent = message;
  notification.className = `fixed top-6 right-6 p-4 rounded-lg ${
    isError ? 'bg-red-500' : 'bg-purple-600'
  } text-white shadow-md transform transition-all duration-300`;
  notification.style.display = 'block';
  setTimeout(() => (notification.style.display = 'none'), 3000);
}

// Generic API call function
async function apiCall(endpoint, method = 'GET', data = null) {
  try {
    const options = {
      method,
      headers: { 'Content-Type': 'application/json' },
    };
    if (data) options.body = JSON.stringify(data);
    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
}

// Build a table for enum items
function buildEnumTable(items, removeCallback) {
  const table = document.createElement('table');
  table.className = 'enum-table';

  const thead = document.createElement('thead');
  thead.innerHTML = `
    <tr>
      <th>Name</th>
      <th>Description</th>
      <th class="action-col">Action</th>
    </tr>
  `;
  table.appendChild(thead);

  const tbody = document.createElement('tbody');
  items.forEach((item) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${item.name}</td>
      <td>${item.description || ''}</td>
      <td class="text-center">
        <button
          class="remove-button"
          data-id="${item.id}"
          type="button"
        >
          Remove
        </button>
      </td>
    `;
    // Attach the remove callback
    const removeBtn = row.querySelector('.remove-button');
    removeBtn.addEventListener('click', (e) => {
      e.preventDefault();
      console.log('Remove button clicked for ID:', item.id);
      removeCallback(item.id);
    });
    tbody.appendChild(row);
  });

  table.appendChild(tbody);

  // Wrap in a container for horizontal scroll if needed
  const wrapper = document.createElement('div');
  wrapper.className = 'table-container';
  wrapper.appendChild(table);

  return wrapper;
}

// Load and display items in a table
async function loadConfigurableItems(endpoint, listId, removeCallback) {
  try {
    const items = await apiCall(endpoint);
    const listContainer = document.getElementById(listId);
    listContainer.innerHTML = '';
    // Build the table and append
    const tableWrapper = buildEnumTable(items, removeCallback);
    listContainer.appendChild(tableWrapper);
  } catch (error) {
    showNotification(`Failed to load ${endpoint}: ` + error.message, true);
  }
}

// Remove Item
async function removeItem(endpoint, id, listId, loadFunction) {
  try {
    console.log(`Removing item with ID ${id} from ${endpoint}`);
    // Ensure proper URL construction with slash
    const url = `${API_BASE_URL}${endpoint}${endpoint.endsWith('/') ? '' : '/'}${id}`;
    console.log('Delete URL:', url);
    
    const response = await fetch(url, { 
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    showNotification('Item removed successfully!');
    loadFunction();
    // Refresh client type dropdown if we're dealing with client types
    if (endpoint === '/client-type/') {
      populateClientTypeDropdown();
    }
  } catch (error) {
    console.error('Error removing item:', error);
    showNotification('Failed to remove item: ' + error.message, true);
  }
}

// Generic Add Form Handler for Configurable Items
async function handleAddConfigurableItem(
  event,
  endpoint,
  listId,
  removeCallback,
  loadFunction
) {
  event.preventDefault();
  const form = event.target;
  const formData = {
    name: form.querySelector('[id$="-name"]').value,
    description: form.querySelector('[id$="-desc"]')?.value || undefined,
  };
  try {
    await apiCall(endpoint, 'POST', formData);
    showNotification(
      `${endpoint.replace('/', '').replace('-', ' ')} added successfully!`
    );
    loadFunction(); // Reload items
    // Refresh client type dropdown if we're dealing with client types
    if (endpoint === '/client-type/') {
      populateClientTypeDropdown();
    }
    form.reset();
  } catch (error) {
    showNotification(
      `Failed to add ${endpoint.replace('/', '').replace('-', ' ')}: ` +
        error.message,
      true
    );
  }
}

// Configuration Form Handler (Create or Update)
async function handleConfigurationSubmit(event, isEdit = false) {
  event.preventDefault();
  const form = event.target;
  const formData = {
    name: form.querySelector(isEdit ? '#edit-config-name' : '#config-name').value,
    client_id: form.querySelector(isEdit ? '#edit-client-id' : '#config-client-id').value,
    client_type_id: parseInt(
      form.querySelector(isEdit ? '#edit-client-type' : '#client-type').value
    ),
    elevenlabs_model:
      form.querySelector(isEdit ? '#edit-elevenlabs-model' : '#elevenlabs-model')
        .value || undefined,
    elevenlabs_voice_id:
      form.querySelector(isEdit ? '#edit-elevenlabs-voice' : '#elevenlabs-voice')
        .value || undefined,
    client_internal_id:
      form.querySelector(isEdit ? '#edit-client-internal-id' : '#client-internal-id')
        .value || undefined,
    twilio_phone_number:
      form.querySelector(isEdit ? '#edit-twilio-phone-number' : '#twilio-phone-number')
        .value || undefined,
    twilio_phone_number_sid:
      form.querySelector(isEdit ? '#edit-twilio-phone-number-sid' : '#twilio-phone-number-sid')
        .value || undefined,
    about_us:
      form.querySelector(isEdit ? '#edit-about-us' : '#about-us').value ||
      undefined,
    services:
      form.querySelector(isEdit ? '#edit-services' : '#services').value ||
      undefined
  };

  const method = isEdit ? 'PUT' : 'POST';
  const endpoint = isEdit
    ? `/configurations/${form.querySelector('#edit-config-id').value}`
    : '/configurations/';

  try {
    console.log('Submitting configuration with data:', formData);
    const result = await apiCall(endpoint, method, formData);
    showNotification(
      isEdit
        ? 'Configuration updated successfully!'
        : 'Configuration created successfully!'
    );
    // If new config, reveal related-entities forms
    if (!isEdit) {
      document.getElementById('related-entities').classList.remove('hidden');
      ['provider', 'request', 'location', 'user'].forEach((prefix) => {
        document.getElementById(`${prefix}-config-id`).value = result.id;
      });
    }
    loadConfigurations();
    if (!isEdit) form.reset();
  } catch (error) {
    console.error('Configuration submission error:', error);
    showNotification(
      `Failed to ${isEdit ? 'update' : 'create'} configuration: ` +
        error.message,
      true
    );
  }
}

// Load Configurations
async function loadConfigurations() {
  try {
    const configs = await apiCall('/configurations/');
    const configList = document.getElementById('config-list');
    configList.innerHTML = '';

    configs.forEach((config) => {
      const card = document.createElement('div');
      card.className = 'config-item flex items-center justify-between gap-4 mb-2';

      // Make the name clickable
      card.innerHTML = `
        <a
          href="edit-config.html?id=${config.id}"
          class="text-gray-700 font-medium underline"
        >
          ${config.name}
        </a>
        <button class="remove-button" data-id="${config.id}">−</button>
      `;

      // Remove button logic
      card.querySelector('.remove-button').addEventListener('click', () =>
        removeItem('/configurations/', config.id, 'config-list', loadConfigurations)
      );

      configList.appendChild(card);
    });
  } catch (error) {
    showNotification('Failed to load configurations: ' + error.message, true);
  }
}

// Tab Switching
function initializeTabs() {
  const tabButtons = document.querySelectorAll('.tab-button');
  const tabContents = document.querySelectorAll('.tab-content');
  tabButtons.forEach((button) => {
    button.addEventListener('click', () => {
      tabButtons.forEach((btn) => btn.classList.remove('active'));
      button.classList.add('active');
      tabContents.forEach((content) => content.classList.add('hidden'));
      document
        .getElementById(button.getAttribute('data-tab'))
        .classList.remove('hidden');
    });
  });
  document.getElementById('add-config-btn').addEventListener('click', () => {
    document.querySelector('[data-tab="add-config"]').click();
  });
}

// Initialize form toggles
function initializeFormToggles() {
  const toggles = [
    {
      toggleBtnId: 'toggle-client-type-form',
      formContainerId: 'client-type-form-container',
    },
    {
      toggleBtnId: 'toggle-user-role-form',
      formContainerId: 'user-role-form-container',
    },
    {
      toggleBtnId: 'toggle-provider-type-form',
      formContainerId: 'provider-type-form-container',
    },
    {
      toggleBtnId: 'toggle-interactor-role-form',
      formContainerId: 'interactor-role-form-container',
    },
    {
      toggleBtnId: 'toggle-pet-type-form',
      formContainerId: 'pet-type-form-container',
    },
    {
      toggleBtnId: 'toggle-sex-form',
      formContainerId: 'sex-form-container',
    },
    {
      toggleBtnId: 'toggle-interaction-category-form',
      formContainerId: 'interaction-category-form-container',
    }
  ];

  toggles.forEach(({ toggleBtnId, formContainerId }) => {
    const toggleBtn = document.getElementById(toggleBtnId);
    const formContainer = document.getElementById(formContainerId);
    if (toggleBtn && formContainer) {
      toggleBtn.addEventListener('click', () => {
        formContainer.classList.toggle('hidden');
      });
    }
  });
}

// Populate Client Type Dropdown
async function populateClientTypeDropdown() {
  try {
    const clientTypes = await apiCall('/client-type/');
    const dropdown = document.getElementById('client-type');
    if (dropdown) {
      dropdown.innerHTML = `
        <option value="">Select a client type</option>
        ${clientTypes.map(type => `<option value="${type.id}">${type.name}</option>`).join('')}
      `;
    }
  } catch (error) {
    showNotification('Failed to load client types: ' + error.message, true);
  }
}

// Initialize everything once the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM Content Loaded');
  initializeTabs();
  initializeFormToggles();
  loadConfigurations();
  populateClientTypeDropdown();

  // Load each Enum table
  loadConfigurableItems('/client-type/', 'client-type-list', (id) =>
    removeItem('/client-type/', id, 'client-type-list', () =>
      loadConfigurableItems('/client-type/', 'client-type-list')
    )
  );
  loadConfigurableItems('/user-role/', 'user-role-list', (id) =>
    removeItem('/user-role/', id, 'user-role-list', () =>
      loadConfigurableItems('/user-role/', 'user-role-list')
    )
  );
  loadConfigurableItems('/provider-type/', 'provider-type-list', (id) =>
    removeItem('/provider-type/', id, 'provider-type-list', () =>
      loadConfigurableItems('/provider-type/', 'provider-type-list')
    )
  );
  loadConfigurableItems('/interactor-role/', 'interactor-role-list', (id) =>
    removeItem('/interactor-role/', id, 'interactor-role-list', () =>
      loadConfigurableItems('/interactor-role/', 'interactor-role-list')
    )
  );
  loadConfigurableItems('/pet-type/', 'pet-type-list', (id) =>
    removeItem('/pet-type/', id, 'pet-type-list', () =>
      loadConfigurableItems('/pet-type/', 'pet-type-list')
    )
  );
  loadConfigurableItems('/sex/', 'sex-list', (id) =>
    removeItem('/sex/', id, 'sex-list', () =>
      loadConfigurableItems('/sex/', 'sex-list')
    )
  );
  loadConfigurableItems('/interaction-category/', 'interaction-category-list', (id) =>
    removeItem('/interaction-category/', id, 'interaction-category-list', () =>
      loadConfigurableItems('/interaction-category/', 'interaction-category-list')
    )
  );

  // Handle form submissions for Configurable Items
  document
    .getElementById('add-client-type-form')
    ?.addEventListener('submit', (e) =>
      handleAddConfigurableItem(
        e,
        '/client-type/',
        'client-type-list',
        (id) =>
          removeItem('/client-type/', id, 'client-type-list', () =>
            loadConfigurableItems('/client-type/', 'client-type-list')
          ),
        () => loadConfigurableItems('/client-type/', 'client-type-list')
      )
    );

  document
    .getElementById('add-user-role-form')
    ?.addEventListener('submit', (e) =>
      handleAddConfigurableItem(
        e,
        '/user-role/',
        'user-role-list',
        (id) =>
          removeItem('/user-role/', id, 'user-role-list', () =>
            loadConfigurableItems('/user-role/', 'user-role-list')
          ),
        () => loadConfigurableItems('/user-role/', 'user-role-list')
      )
    );

  document
    .getElementById('add-provider-type-form')
    ?.addEventListener('submit', (e) =>
      handleAddConfigurableItem(
        e,
        '/provider-type/',
        'provider-type-list',
        (id) =>
          removeItem('/provider-type/', id, 'provider-type-list', () =>
            loadConfigurableItems('/provider-type/', 'provider-type-list')
          ),
        () => loadConfigurableItems('/provider-type/', 'provider-type-list')
      )
    );

  document
    .getElementById('add-interactor-role-form')
    ?.addEventListener('submit', (e) =>
      handleAddConfigurableItem(
        e,
        '/interactor-role/',
        'interactor-role-list',
        (id) =>
          removeItem('/interactor-role/', id, 'interactor-role-list', () =>
            loadConfigurableItems('/interactor-role/', 'interactor-role-list')
          ),
        () => loadConfigurableItems('/interactor-role/', 'interactor-role-list')
      )
    );

  document
    .getElementById('add-pet-type-form')
    ?.addEventListener('submit', (e) =>
      handleAddConfigurableItem(
        e,
        '/pet-type/',
        'pet-type-list',
        (id) =>
          removeItem('/pet-type/', id, 'pet-type-list', () =>
            loadConfigurableItems('/pet-type/', 'pet-type-list')
          ),
        () => loadConfigurableItems('/pet-type/', 'pet-type-list')
      )
    );

  document
    .getElementById('add-sex-form')
    ?.addEventListener('submit', (e) =>
      handleAddConfigurableItem(
        e,
        '/sex/',
        'sex-list',
        (id) =>
          removeItem('/sex/', id, 'sex-list', () =>
            loadConfigurableItems('/sex/', 'sex-list')
          ),
        () => loadConfigurableItems('/sex/', 'sex-list')
      )
    );

  document
    .getElementById('add-interaction-category-form')
    ?.addEventListener('submit', (e) =>
      handleAddConfigurableItem(
        e,
        '/interaction-category/',
        'interaction-category-list',
        (id) =>
          removeItem('/interaction-category/', id, 'interaction-category-list', () =>
            loadConfigurableItems('/interaction-category/', 'interaction-category-list')
          ),
        () => loadConfigurableItems('/interaction-category/', 'interaction-category-list')
      )
    );

  // Handle form submissions for creating/editing configurations
  document
    .getElementById('config-form')
    .addEventListener('submit', (e) => handleConfigurationSubmit(e, false));
});
