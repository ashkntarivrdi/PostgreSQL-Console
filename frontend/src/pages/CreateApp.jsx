import React, { useContext, useState } from 'react';
import { Form, Input, InputNumber, Button, Modal, message } from 'antd';
import { AuthContext } from '../context/AuthContext';
import Navbar from '../components/Navbar';

const CreateApp = () => {
  const { token } = useContext(AuthContext);
  const [form] = Form.useForm();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [formData, setFormData] = useState(null);

  const showConfirmationModal = (values) => {
    setFormData(values);
    setIsModalVisible(true);
  };

  const handleOk = async () => {
    setIsModalVisible(false);
    try {
      // Check for duplicate app name
      const checkResponse = await fetch('http://localhost:8000/api/v1/apps/', {
        headers: {
          'Authorization': `${token}`,
        },
      });
      const checkData = await checkResponse.json();
      const isDuplicate = checkData.results.some(app => app.name === formData.name);

      if (isDuplicate) {
        message.error('App name already exists. Please choose a different name.');
        form.resetFields(); 
        return;
      }

      // Proceed with app creation
      const response = await fetch('http://localhost:8000/api/v1/app/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `${token}`,
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        form.resetFields(); 
        throw new Error('App creation failed');
      }

      const data = await response.json();
      message.success(`App "${data.name}" created successfully!`);
      form.resetFields(); 
    } catch (error) {
      message.error(`Error creating app: ${error.message}`);
      form.resetFields(); 
    }
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  const onFinish = (values) => {
    showConfirmationModal(values);
  };

  return (
    <>
      <Navbar />
      <Form form={form} onFinish={onFinish}>
        <Form.Item
          name="name"
          label="App Name"
          rules={[{ required: true, message: 'Please input the app name!' }]}
        >
          <Input placeholder="App Name" />
        </Form.Item>
        <Form.Item
          name="size"
          label="App Size"
          rules={[{ required: true, message: 'Please input the app size!' }]}
        >
          <InputNumber min={1} max={2000} placeholder="App Size" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit">
            Create App
          </Button>
        </Form.Item>
      </Form>

      <Modal
        title="Confirm App Creation"
        visible={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        <p>Are you sure you want to create the app with the following details?</p>
        <p>Name: {formData?.name}</p>
        <p>Size: {formData?.size}</p>
      </Modal>
    </>
  );
};

export default CreateApp;
