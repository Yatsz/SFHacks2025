import { collection, getDocs } from 'firebase/firestore';
import { db } from '../firebase';
import { FamilyMember } from '../models/FamilyMember';

export async function getAllFamilyMembers(): Promise<FamilyMember[]> {
  const querySnapshot = await getDocs(collection(db, 'family'));
  return querySnapshot.docs.map(doc => ({
    id: doc.id,
    ...doc.data()
  } as FamilyMember));
} 