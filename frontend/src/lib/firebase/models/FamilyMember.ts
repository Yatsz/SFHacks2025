export interface FamilyMember {
  id?: string;
  color: string;
  image: string; // Base64URL encoded image
  isAdmin: boolean;
  name: string;
  relationship: string;
} 