'use client';

import React, { createContext, useContext, ReactNode } from 'react';
import { db, auth, storage } from './firebase';
import { User } from 'firebase/auth';
import { Firestore } from 'firebase/firestore';
import { FirebaseStorage } from 'firebase/storage';

// Define the shape of the context
interface FirebaseContextType {
  db: Firestore;
  auth: {
    currentUser: User | null;
    // Add any other auth functions you need
  };
  storage: FirebaseStorage;
}

// Create the context with a default value
const FirebaseContext = createContext<FirebaseContextType | undefined>(undefined);

interface FirebaseProviderProps {
  children: ReactNode;
}

// Create a provider component
export function FirebaseProvider({ children }: FirebaseProviderProps) {
  // Initialize Firebase objects
  const firebaseAuth = {
    currentUser: auth.currentUser,
    // Add any other auth functions here
  };

  const value = {
    db,
    auth: firebaseAuth,
    storage,
  };

  return (
    <FirebaseContext.Provider value={value}>
      {children}
    </FirebaseContext.Provider>
  );
}

// Create a custom hook to use the Firebase context
export function useFirebase() {
  const context = useContext(FirebaseContext);
  if (context === undefined) {
    throw new Error('useFirebase must be used within a FirebaseProvider');
  }
  return context;
} 