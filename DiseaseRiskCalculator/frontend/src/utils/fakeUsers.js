// src/utils/fakeUsers.js

let fakeUsers = [
    { id: 1, email: 'admin@example.com', password: 'admin123', role: 'admin', active: true },
    { id: 2, email: 'doctor@example.com', password: 'doctor123', role: 'doctor', active: true },
    { id: 3, email: 'patient@example.com', password: 'patient123', role: 'patient', active: true },
  ];
  
  let nextId = 4;
  
  export function authenticateUser(email, password) {
    const user = fakeUsers.find(u => u.email === email && u.password === password && u.active);
    if (user) {
      const { password, ...userWithoutPassword } = user;
      return userWithoutPassword;
    }
    return null;
  }
  
  export function addUser(userData) {
    if (fakeUsers.some(user => user.email === userData.email)) {
      throw new Error('User already exists');
    }
    const newUser = { ...userData, id: nextId++, active: true };
    fakeUsers.push(newUser);
  }

  export function updateUser(userId, userData) {
    const userIndex = fakeUsers.findIndex(user => user.id === userId);
    if (userIndex !== -1) {
      fakeUsers[userIndex] = { ...fakeUsers[userIndex], ...userData };
      return true;
    }
    return false;
  }
  
  export function getAllUsers() {
    return fakeUsers.map(({ password, ...user }) => user);
  }
  
  export function updateUserStatus(userId, active) {
    const userIndex = fakeUsers.findIndex(user => user.id === userId);
    if (userIndex !== -1) {
      fakeUsers[userIndex].active = active;
      return true;
    }
    return false;
  }