import {
  collection,
  doc,
  setDoc,
  getDoc,
  getDocs,
  query,
  where,
  orderBy,
  limit,
  updateDoc,
  deleteDoc,
  addDoc,
  DocumentData,
  QueryDocumentSnapshot,
  SnapshotOptions,
  FirestoreDataConverter,
  WithFieldValue,
  serverTimestamp,
  WhereFilterOp,
} from 'firebase/firestore';
import { db } from './firebase';

// Define a base document interface to enforce ID field
export interface BaseDocument {
  id?: string;
  [key: string]: unknown;
}

// Generic firestore converter
export function createConverter<T extends BaseDocument>(): FirestoreDataConverter<T> {
  return {
    toFirestore(data: WithFieldValue<T>): DocumentData {
      return { ...data, updatedAt: serverTimestamp() };
    },
    fromFirestore(
      snapshot: QueryDocumentSnapshot,
      options?: SnapshotOptions
    ): T {
      const data = snapshot.data(options);
      return { ...data, id: snapshot.id } as unknown as T;
    },
  };
}

// Generic function to get a collection reference with type safety
export function getCollectionRef<T extends BaseDocument>(collectionPath: string) {
  return collection(db, collectionPath).withConverter(createConverter<T>());
}

// Generic function to get a document reference with type safety
export function getDocRef<T extends BaseDocument>(collectionPath: string, docId: string) {
  return doc(db, collectionPath, docId).withConverter(createConverter<T>());
}

// CRUD Operations

// Create a document with a specific ID
export async function createDocument<T extends BaseDocument>(
  collectionPath: string,
  docId: string,
  data: WithFieldValue<T>
) {
  const docRef = getDocRef<T>(collectionPath, docId);
  await setDoc(docRef, { ...data, createdAt: serverTimestamp() });
  return docId;
}

// Create a document with auto-generated ID
export async function addDocument<T extends BaseDocument>(
  collectionPath: string,
  data: WithFieldValue<T>
) {
  const collectionRef = getCollectionRef<T>(collectionPath);
  const docRef = await addDoc(collectionRef, { ...data, createdAt: serverTimestamp() });
  return docRef.id;
}

// Read a document
export async function getDocument<T extends BaseDocument>(
  collectionPath: string,
  docId: string
): Promise<T | null> {
  const docRef = getDocRef<T>(collectionPath, docId);
  const docSnap = await getDoc(docRef);
  
  if (docSnap.exists()) {
    return docSnap.data();
  } else {
    return null;
  }
}

// Update a document
export async function updateDocument<T extends BaseDocument>(
  collectionPath: string,
  docId: string,
  data: Partial<T>
) {
  const docRef = getDocRef<T>(collectionPath, docId);
  await updateDoc(docRef, data as DocumentData);
}

// Delete a document
export async function deleteDocument(
  collectionPath: string,
  docId: string
) {
  const docRef = doc(db, collectionPath, docId);
  await deleteDoc(docRef);
}

// Get all documents from a collection
export async function getCollection<T extends BaseDocument>(
  collectionPath: string
): Promise<T[]> {
  const collectionRef = getCollectionRef<T>(collectionPath);
  const querySnapshot = await getDocs(collectionRef);
  
  return querySnapshot.docs.map(doc => doc.data());
}

// Query documents with conditions
export async function queryDocuments<T extends BaseDocument>(
  collectionPath: string,
  conditions: Array<{
    field: string;
    operator: WhereFilterOp;
    value: unknown;
  }>,
  orderByField?: string,
  orderDirection?: 'asc' | 'desc',
  limitCount?: number
): Promise<T[]> {
  const collectionRef = getCollectionRef<T>(collectionPath);
  
  let q = query(
    collectionRef,
    ...conditions.map(cond => where(cond.field, cond.operator, cond.value))
  );
  
  if (orderByField) {
    q = query(q, orderBy(orderByField, orderDirection || 'asc'));
  }
  
  if (limitCount) {
    q = query(q, limit(limitCount));
  }
  
  const querySnapshot = await getDocs(q);
  return querySnapshot.docs.map(doc => doc.data());
} 