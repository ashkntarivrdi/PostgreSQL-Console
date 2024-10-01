import React, { useState, useEffect, useContext } from 'react';
import { useParams } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import { Descriptions, InputNumber, Button } from 'antd';

const AppDetails = () => {
  const { id } = useParams();
  const { token } = useContext(AuthContext);
  const [app, setApp] = useState(null);
  const [newSize, setNewSize] = useState(null);

  useEffect(() => {
    const fetchAppDetails = async () => {
      const response = await fetch(`http://localhost:8000/api/v1/app/${id}/`, {
        headers: {
          'Authorization': `${token}`,
        },
      });
      const data = await response.json();
      if (response.ok) {
        setApp(data);
      } else {
        console.error('Error fetching app details:', data.error);
      }
    };

    fetchAppDetails();
  }, [id, token]);

  const handleSizeUpdate = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/app/${id}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `${token}`,
        },
        body: JSON.stringify({ size: newSize }),
      });
      const data = await response.json();
      if (response.ok) {
        setApp(data);
        setNewSize(null); // Reset the size input
      } else {
        console.error('Error updating app size:', data.error);
      }
    } catch (error) {
      console.error('Error updating app size:', error);
    }
  };

  if (!app) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <Navbar />        
      <Descriptions title="App Details">
        <Descriptions.Item label="Name">{app.name}</Descriptions.Item>
        <Descriptions.Item label="State">{app.state}</Descriptions.Item>
        <Descriptions.Item label="Creation Time">{app.creation_time}</Descriptions.Item>
        <Descriptions.Item label="Size">
          <InputNumber
            min={app.size + 1}
            max={2000}
            value={newSize || app.size}
            onChange={setNewSize}
          />
          <Button onClick={handleSizeUpdate} type="primary" style={{ marginLeft: '10px' }}>
            Update Size
          </Button>
        </Descriptions.Item>
      </Descriptions>
    </div>
  );
};

export default AppDetails;
