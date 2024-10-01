import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';
import { Menu } from 'antd';

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login'); 
  };

  return (
    <Menu mode="horizontal">
      <Menu.Item key="main">
        <Link to="/main">Databases</Link>
      </Menu.Item>
      <Menu.Item key="create">
        <Link to="/create">Create Database</Link>
      </Menu.Item>
      <Menu.Item key="app-details">
        <Link to="/app/:id">App Details</Link>
      </Menu.Item>
      <Menu.Item key="user" style={{ marginLeft: 'auto' }}>
        {user?.username || 'Guest'}
      </Menu.Item>
      {user && (
        <Menu.Item key="logout" onClick={handleLogout}>
          Logout
        </Menu.Item>
      )}
    </Menu>
  );
};

export default Navbar;
