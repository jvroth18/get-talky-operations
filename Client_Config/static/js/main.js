// main.js

// API Base URL - Update this to point to your backend server
const API_BASE_URL = '/api'; // Use relative path for both development and production

// Function to initialize all components
function initializeAllComponents() {
    console.log('Initializing all components');
    initializeTabs();
    initializeFormToggles();
    loadConfigurations();
    populateClientTypeDropdown();
    initializeEnumForms();
    initializeEditConfigPage();
    
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
}

// Function to initialize enum form submissions
function initializeEnumForms() {
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
        ?.addEventListener('submit', (e) => handleConfigurationSubmit(e, false));
}

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

// Handle browser navigation events
window.onpopstate = function(event) {
    console.log('Navigation occurred, reinitializing components');
    initializeAllComponents();
};

// Initialize everything once the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded');
    initializeAllComponents();
});

// Function to build a provider table
function buildProviderTable(providers) {
    const table = document.createElement('table');
    table.className = 'data-table w-full';
    
    const thead = document.createElement('thead');
    thead.innerHTML = `
        <tr>
            <th>Name</th>
            <th>Provider Type</th>
            <th>Request Types</th>
            <th>Phone</th>
            <th>Email</th>
            <th>Actions</th>
        </tr>
    `;
    table.appendChild(thead);
    
    const tbody = document.createElement('tbody');
    if (providers.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="6" class="text-center py-4">No providers found</td>';
        tbody.appendChild(row);
    } else {
        providers.forEach(provider => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${provider.first_name} ${provider.last_name}</td>
                <td>${provider.provider_type?.name || ''}</td>
                <td>${provider.request_types?.map(rt => rt.name).join(', ') || ''}</td>
                <td>${provider.phone_number || ''}</td>
                <td>${provider.email || ''}</td>
                <td>
                    <button class="remove-button" data-id="${provider.id}">Remove</button>
                </td>
            `;
            
            row.querySelector('.remove-button').addEventListener('click', () => {
                removeItem('/providers/', provider.id, 'providers-list', () => loadConfigData());
            });
            
            tbody.appendChild(row);
        });
    }
    
    table.appendChild(tbody);
    return table;
}

// Function to build a request types table
function buildRequestTypesTable(requestTypes) {
    const table = document.createElement('table');
    table.className = 'data-table w-full';
    
    const thead = document.createElement('thead');
    thead.innerHTML = `
        <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Length</th>
            <th>Actions</th>
        </tr>
    `;
    table.appendChild(thead);
    
    const tbody = document.createElement('tbody');
    if (requestTypes.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="4" class="text-center py-4">No request types found</td>';
        tbody.appendChild(row);
    } else {
        requestTypes.forEach(rt => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${rt.name}</td>
                <td>${rt.description || ''}</td>
                <td>${rt.length || ''}</td>
                <td>
                    <button class="remove-button" data-id="${rt.id}">Remove</button>
                </td>
            `;
            
            row.querySelector('.remove-button').addEventListener('click', () => {
                removeItem('/request_types/', rt.id, 'request-types-list', () => loadConfigData());
            });
            
            tbody.appendChild(row);
        });
    }
    
    table.appendChild(tbody);
    return table;
}

// Function to build a locations table
function buildLocationsTable(locations) {
    const table = document.createElement('table');
    table.className = 'data-table w-full';
    
    const thead = document.createElement('thead');
    thead.innerHTML = `
        <tr>
            <th>Name</th>
            <th>Phone</th>
            <th>Operating Hours</th>
            <th>Address</th>
            <th>Actions</th>
        </tr>
    `;
    table.appendChild(thead);
    
    const tbody = document.createElement('tbody');
    if (locations.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="5" class="text-center py-4">No locations found</td>';
        tbody.appendChild(row);
    } else {
        locations.forEach(location => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${location.name}</td>
                <td>${location.phone_number || ''}</td>
                <td>${location.operating_hours || ''}</td>
                <td>${location.address || ''}</td>
                <td>
                    <button class="remove-button" data-id="${location.id}">Remove</button>
                </td>
            `;
            
            row.querySelector('.remove-button').addEventListener('click', () => {
                removeItem('/locations/', location.id, 'locations-list', () => loadConfigData());
            });
            
            tbody.appendChild(row);
        });
    }
    
    table.appendChild(tbody);
    return table;
}

// Function to build an API keys table
function buildApiKeysTable(apiKeys) {
    const table = document.createElement('table');
    table.className = 'data-table w-full';
    
    const thead = document.createElement('thead');
    thead.innerHTML = `
        <tr>
            <th>Name</th>
            <th>API Key</th>
            <th>Actions</th>
        </tr>
    `;
    table.appendChild(thead);
    
    const tbody = document.createElement('tbody');
    if (apiKeys.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="3" class="text-center py-4">No API keys found</td>';
        tbody.appendChild(row);
    } else {
        apiKeys.forEach(key => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${key.name}</td>
                <td>${key.api_key}</td>
                <td>
                    <button class="remove-button" data-id="${key.id}">Remove</button>
                </td>
            `;
            
            row.querySelector('.remove-button').addEventListener('click', () => {
                removeItem('/client_api_keys/', key.id, 'api-keys-list', () => loadConfigData());
            });
            
            tbody.appendChild(row);
        });
    }
    
    table.appendChild(tbody);
    return table;
}

// Function to build a users table
function buildUsersTable(users) {
    const table = document.createElement('table');
    table.className = 'data-table w-full';
    
    const thead = document.createElement('thead');
    thead.innerHTML = `
        <tr>
            <th>Name</th>
            <th>Phone</th>
            <th>Email</th>
            <th>Role</th>
            <th>Actions</th>
        </tr>
    `;
    table.appendChild(thead);
    
    const tbody = document.createElement('tbody');
    if (users.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="5" class="text-center py-4">No users found</td>';
        tbody.appendChild(row);
    } else {
        users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${user.first_name} ${user.last_name}</td>
                <td>${user.phone_number || ''}</td>
                <td>${user.email || ''}</td>
                <td>${user.role?.name || ''}</td>
                <td>
                    <button class="remove-button" data-id="${user.id}">Remove</button>
                </td>
            `;
            
            row.querySelector('.remove-button').addEventListener('click', () => {
                removeItem('/users/', user.id, 'users-list', () => loadConfigData());
            });
            
            tbody.appendChild(row);
        });
    }
    
    table.appendChild(tbody);
    return table;
}

// Function to load all configuration data
async function loadConfigData() {
    const urlParams = new URLSearchParams(window.location.search);
    const configId = urlParams.get('id');
    if (!configId) {
        console.log('No config ID found in URL');
        return;
    }

    console.log('Loading config data for ID:', configId);

    // Initialize localData object if it doesn't exist
    window.localData = window.localData || {};

    // Load all data types
    await Promise.all([
        loadProviders(configId),
        loadRequestTypes(configId),
        loadLocations(configId),
        loadApiKeys(configId),
        loadUsers(configId)
    ]).catch(error => {
        console.error('Error loading some data:', error);
        showNotification('Some data failed to load. Please check the console for details.', true);
    });
}

// Function to initialize edit config page
function initializeEditConfigPage() {
    const urlParams = new URLSearchParams(window.location.search);
    const configId = urlParams.get('id');
    if (configId) {
        console.log('Initializing edit config page for ID:', configId);
        loadConfigData();
    }
}

// Functions to load related entities
async function loadProviders(configId) {
  try {
    const response = await fetch(`${API_BASE_URL}/providers/${configId}`);
    if (!response.ok) throw new Error('Failed to fetch providers');
    const providers = await response.json();
    localData.providers = providers;
    
    // Get provider types for mapping
    const providerTypesResponse = await fetch(`${API_BASE_URL}/provider-type/`);
    if (!providerTypesResponse.ok) throw new Error('Failed to fetch provider types');
    const providerTypes = await providerTypesResponse.json();
    const providerTypeMap = Object.fromEntries(providerTypes.map(type => [type.id, type.name]));

    // Get request types for mapping
    const requestTypesResponse = await fetch(`${API_BASE_URL}/request_types/${configId}`);
    if (!requestTypesResponse.ok) throw new Error('Failed to fetch request types');
    const requestTypes = await requestTypesResponse.json();
    const requestTypeMap = Object.fromEntries(requestTypes.map(type => [type.id, type.name]));
    
    const tbody = document.getElementById('providers-list');
    tbody.innerHTML = providers.map(provider => {
      // Get request types for this provider
      const providerRequestTypes = provider.request_types || [];
      const requestTypeNames = providerRequestTypes
        .map(rt => requestTypeMap[rt.id])
        .filter(name => name) // Filter out undefined values
        .join(', ');

      return `
        <tr class="hover:bg-gray-50">
          <td class="px-6 py-4">${provider.first_name} ${provider.last_name}</td>
          <td class="px-6 py-4">${provider.provider_type_id ? providerTypeMap[provider.provider_type_id] : '-'}</td>
          <td class="px-6 py-4">${requestTypeNames || '-'}</td>
          <td class="px-6 py-4">${provider.phone_number || '-'}</td>
          <td class="px-6 py-4">${provider.email || '-'}</td>
          <td class="px-6 py-4">
            <button onclick="deleteProvider(${provider.id})" 
                    class="text-red-600 hover:text-red-800 font-medium">
              Delete
            </button>
          </td>
        </tr>
      `;
    }).join('');
  } catch (error) {
    console.error('Error loading providers:', error);
    showNotification('Error loading providers: ' + error.message, true);
  }
}

async function loadRequestTypes(configId) {
  try {
    const response = await fetch(`${API_BASE_URL}/request_types/${configId}`);
    if (!response.ok) throw new Error('Failed to fetch request types');
    const requestTypes = await response.json();
    localData.requestTypes = requestTypes;
    
    const tbody = document.getElementById('request-types-list');
    tbody.innerHTML = requestTypes.map(type => `
      <tr class="hover:bg-gray-50">
        <td class="px-6 py-4">${type.name}</td>
        <td class="px-6 py-4">${type.description || '-'}</td>
        <td class="px-6 py-4">${type.length || '-'}</td>
        <td class="px-6 py-4">
          <button onclick="deleteRequestType(${type.id})" 
                  class="text-red-600 hover:text-red-800 font-medium">
            Delete
          </button>
        </td>
      </tr>
    `).join('');
  } catch (error) {
    showNotification('Error loading request types: ' + error.message, true);
  }
}

async function loadLocations(configId) {
  try {
    const response = await fetch(`${API_BASE_URL}/locations/${configId}`);
    if (!response.ok) throw new Error('Failed to fetch locations');
    const locations = await response.json();
    localData.locations = locations;
    
    const tbody = document.getElementById('locations-list');
    tbody.innerHTML = locations.map(location => `
      <tr class="hover:bg-gray-50">
        <td class="px-6 py-4">${location.name}</td>
        <td class="px-6 py-4">${location.phone_number || '-'}</td>
        <td class="px-6 py-4">${location.operating_hours || '-'}</td>
        <td class="px-6 py-4">${location.address || '-'}</td>
        <td class="px-6 py-4">
          <button onclick="deleteLocation(${location.id})" 
                  class="text-red-600 hover:text-red-800 font-medium">
            Delete
          </button>
        </td>
      </tr>
    `).join('');
  } catch (error) {
    showNotification('Error loading locations: ' + error.message, true);
  }
}

async function loadApiKeys(configId) {
  try {
    const response = await fetch(`${API_BASE_URL}/client_api_keys/${configId}`);
    if (!response.ok) throw new Error('Failed to fetch API keys');
    const apiKeys = await response.json();
    localData.apiKeys = apiKeys;
    
    const tbody = document.getElementById('api-keys-list');
    tbody.innerHTML = apiKeys.map(key => `
      <tr class="hover:bg-gray-50">
        <td class="px-6 py-4">${key.name}</td>
        <td class="px-6 py-4">${key.api_key}</td>
        <td class="px-6 py-4">
          <span class="px-2 py-1 rounded-full text-xs font-medium
                     ${key.active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
            ${key.active ? 'Active' : 'Inactive'}
          </span>
        </td>
        <td class="px-6 py-4">
          <button onclick="deleteApiKey(${key.id})" 
                  class="text-red-600 hover:text-red-800 font-medium">
            Delete
          </button>
        </td>
      </tr>
    `).join('');
  } catch (error) {
    showNotification('Error loading API keys: ' + error.message, true);
  }
}

async function loadUsers(configId) {
  try {
    const response = await fetch(`${API_BASE_URL}/users/${configId}`);
    if (!response.ok) throw new Error('Failed to fetch users');
    const users = await response.json();
    localData.users = users;
    
    const tbody = document.getElementById('users-list');
    tbody.innerHTML = users.map(user => `
      <tr class="hover:bg-gray-50">
        <td class="px-6 py-4">${user.first_name} ${user.last_name}</td>
        <td class="px-6 py-4">${user.phone_number || '-'}</td>
        <td class="px-6 py-4">${user.email || '-'}</td>
        <td class="px-6 py-4">${user.role?.name || '-'}</td>
        <td class="px-6 py-4">
          <button onclick="deleteUser(${user.id})" 
                  class="text-red-600 hover:text-red-800 font-medium">
            Delete
          </button>
        </td>
      </tr>
    `).join('');
  } catch (error) {
    showNotification('Error loading users: ' + error.message, true);
  }
}

// Delete functions for related entities
async function deleteProvider(id) {
  if (!confirm('Are you sure you want to delete this provider?')) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/providers/${id}`, { method: 'DELETE' });
    if (!response.ok) throw new Error('Failed to delete provider');
    await loadProviders(configId);
    showNotification('Provider deleted successfully');
  } catch (error) {
    showNotification('Failed to delete provider: ' + error.message, true);
  }
}

async function deleteRequestType(id) {
  if (!confirm('Are you sure you want to delete this request type?')) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/request_types/${id}`, { method: 'DELETE' });
    if (!response.ok) throw new Error('Failed to delete request type');
    await loadRequestTypes(configId);
    showNotification('Request type deleted successfully');
  } catch (error) {
    showNotification('Failed to delete request type: ' + error.message, true);
  }
}

async function deleteLocation(id) {
  if (!confirm('Are you sure you want to delete this location?')) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/locations/${id}`, { method: 'DELETE' });
    if (!response.ok) throw new Error('Failed to delete location');
    await loadLocations(configId);
    showNotification('Location deleted successfully');
  } catch (error) {
    showNotification('Failed to delete location: ' + error.message, true);
  }
}

async function deleteApiKey(id) {
  if (!confirm('Are you sure you want to delete this API key?')) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/client_api_keys/${id}`, { method: 'DELETE' });
    if (!response.ok) throw new Error('Failed to delete API key');
    await loadApiKeys(configId);
    showNotification('API key deleted successfully');
  } catch (error) {
    showNotification('Failed to delete API key: ' + error.message, true);
  }
}

async function deleteUser(id) {
  if (!confirm('Are you sure you want to delete this user?')) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/users/${id}`, { method: 'DELETE' });
    if (!response.ok) throw new Error('Failed to delete user');
    await loadUsers(configId);
    showNotification('User deleted successfully');
  } catch (error) {
    showNotification('Failed to delete user: ' + error.message, true);
  }
}

// Modal trigger functions
function showAddProviderModal() {
  // Load both provider types and request types before showing modal
  Promise.all([
    loadProviderTypes(),
    loadRequestTypesForSelect()
  ]).then(() => {
    showModal('provider-modal');
  }).catch(error => {
    console.error('Error loading form data:', error);
    showNotification('Failed to load form data', true);
  });
}

// Function to load provider types
async function loadProviderTypes() {
  try {
    const response = await fetch(`${API_BASE_URL}/provider-type/`);
    if (!response.ok) throw new Error('Failed to fetch provider types');
    const providerTypes = await response.json();
    
    const providerTypeSelect = document.querySelector('#provider-modal select[name="provider_type_id"]');
    if (providerTypeSelect) {
      providerTypeSelect.innerHTML = `
        <option value="">Select a provider type</option>
        ${providerTypes.map(type => `<option value="${type.id}">${type.name}</option>`).join('')}
      `;
    } else {
      throw new Error('Provider type select element not found');
    }
  } catch (error) {
    console.error('Error loading provider types:', error);
    throw error;
  }
}

// Add function to load request types for the select
async function loadRequestTypesForSelect() {
  try {
    const response = await fetch(`${API_BASE_URL}/request_types/${configId}`);
    if (!response.ok) throw new Error('Failed to fetch request types');
    const requestTypes = await response.json();
    
    const requestTypeSelect = document.querySelector('#provider-modal select[name="request_type_ids"]');
    if (requestTypeSelect) {
      requestTypeSelect.innerHTML = requestTypes
        .map(type => `<option value="${type.id}">${type.name}</option>`)
        .join('');
    } else {
      throw new Error('Request type select element not found');
    }
  } catch (error) {
    console.error('Error loading request types:', error);
    throw error;
  }
}
