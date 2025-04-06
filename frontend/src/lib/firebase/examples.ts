import { 
  addDocument,
  getDocument,
  updateDocument,
  deleteDocument,
  getCollection,
  queryDocuments,
  BaseDocument 
} from './firestore';
import { Timestamp, WithFieldValue } from 'firebase/firestore';

// Example type definitions for your collections
export interface User extends BaseDocument {
  name: string;
  email: string;
  photoURL?: string;
  createdAt?: Timestamp;
  updatedAt?: Timestamp;
}

export interface Family extends BaseDocument {
  name: string;
  members: string[]; // User IDs
  createdAt?: Timestamp;
  updatedAt?: Timestamp;
}

// Example collection constants
export const COLLECTIONS = {
  USERS: 'users',
  FAMILIES: 'families',
  MEMORIES: 'memories',
  ROUTINES: 'routines',
  REMINDERS: 'reminders',
};

// Example functions for a User collection

// Add a new user
export async function createUser(userData: {
  name: string;
  email: string;
  photoURL?: string;
}) {
  return await addDocument<User>(COLLECTIONS.USERS, userData as WithFieldValue<User>);
}

// Get a user by ID
export async function getUserById(userId: string) {
  return await getDocument<User>(COLLECTIONS.USERS, userId);
}

// Update a user
export async function updateUser(userId: string, userData: Partial<User>) {
  await updateDocument<User>(COLLECTIONS.USERS, userId, userData);
}

// Delete a user
export async function deleteUser(userId: string) {
  await deleteDocument(COLLECTIONS.USERS, userId);
}

// Get all users
export async function getAllUsers() {
  return await getCollection<User>(COLLECTIONS.USERS);
}

// Query users by conditions
export async function queryUsersByName(name: string) {
  return await queryDocuments<User>(
    COLLECTIONS.USERS,
    [{ field: 'name', operator: '==', value: name }]
  );
}

// Example functions for a Family collection

// Add a new family
export async function createFamily(familyData: {
  name: string;
  members: string[];
}) {
  return await addDocument<Family>(COLLECTIONS.FAMILIES, familyData as WithFieldValue<Family>);
}

// Get a family by ID
export async function getFamilyById(familyId: string) {
  return await getDocument<Family>(COLLECTIONS.FAMILIES, familyId);
}

// Add a member to a family
export async function addMemberToFamily(familyId: string, userId: string) {
  const family = await getDocument<Family>(COLLECTIONS.FAMILIES, familyId);
  if (family && !family.members.includes(userId)) {
    const updatedMembers = [...family.members, userId];
    await updateDocument<Family>(COLLECTIONS.FAMILIES, familyId, { members: updatedMembers });
  }
}

// Remove a member from a family
export async function removeMemberFromFamily(familyId: string, userId: string) {
  const family = await getDocument<Family>(COLLECTIONS.FAMILIES, familyId);
  if (family) {
    const updatedMembers = family.members.filter(id => id !== userId);
    await updateDocument<Family>(COLLECTIONS.FAMILIES, familyId, { members: updatedMembers });
  }
} 