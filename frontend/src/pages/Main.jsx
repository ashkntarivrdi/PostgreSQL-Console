import React, { useContext, useState, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import { Input, List, Button, Modal, message } from 'antd';

const { Search } = Input;

const Main = () => {
  const { token } = useContext(AuthContext);
  const [apps, setApps] = useState([]);
  const [filteredApps, setFilteredApps] = useState([]);
  const [appToDelete, setAppToDelete] = useState(null); 

  useEffect(() => {
    const fetchApps = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/apps/', {
          headers: {
            'Authorization': `${token}`,
          },
        });
        const data = await response.json();
        if (response.ok) {
          setApps(data.results);
          setFilteredApps(data.results);
        } else {
          console.error('Error fetching apps:', data.error);
          message.error('Failed to fetch apps.');
        }
      } catch (error) {
        console.error('Error fetching apps:', error);
        message.error('Error occurred while fetching apps.');
      }
    };

    fetchApps();

    const intervalId = setInterval(fetchApps, 5000);

    return () => clearInterval(intervalId);
  }, [token]);

  const handleDelete = async () => {
    if (!appToDelete) return;

    try {
      const response = await fetch(`http://localhost:8000/api/v1/app/${appToDelete.id}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `${token}`,
        },
      });
      if (response.ok) {
        message.success('App deleted successfully');
        setApps(prevApps => prevApps.filter(app => app.id !== appToDelete.id));
        setFilteredApps(prevApps => prevApps.filter(app => app.id !== appToDelete.id));
        setAppToDelete(null);
      } else {
        const data = await response.json();
        console.error('Error deleting app:', data.error);
        message.error('Failed to delete app.');
      }
    } catch (error) {
      console.error('Error deleting app:', error);
      message.error('Error occurred while deleting the app.');
    }
  };

  const showConfirmDelete = (app) => {
    setAppToDelete(app); 
    Modal.confirm({
      title: `Are you sure you want to delete '${app.name}'?`,
      okText: 'Delete',
      okType: 'danger',
      cancelText: 'Cancel',
      onOk: handleDelete,
      onCancel: () => setAppToDelete(null),
    });
  };

  const filterApps = (query) => {
    setFilteredApps(apps.filter(app => app.name.toLowerCase().includes(query.toLowerCase())));
  };

  return (
    <div style={{ padding: '20px' }}>
      <Navbar />
      <h1>Your Apps</h1>
      <Search
        placeholder="Search apps..."
        onChange={e => filterApps(e.target.value)}
        style={{ marginBottom: '20px' }}
      />
      <List
        itemLayout="horizontal"
        dataSource={filteredApps}
        renderItem={app => (
          <List.Item
            actions={[
              <Button type="primary" danger onClick={() => showConfirmDelete(app)}>
                Delete
              </Button>
            ]}
          >
            <List.Item.Meta
              title={app.name}
              description={`Status: ${app.state}`}
            />
          </List.Item>
        )}
      />
    </div>
  );
};

export default Main;
