'use client';

import { useState, useEffect } from 'react';
import { getAllFamilyMembers } from '../../lib/firebase/services/familyService';
import { FamilyMember } from '../../lib/firebase/models/FamilyMember';
import Link from 'next/link';

interface FamilyMembersClientProps {
  onLoaded?: (members: FamilyMember[]) => void;
}

export default function FamilyMembersClient({ onLoaded }: FamilyMembersClientProps) {
  const [familyMembers, setFamilyMembers] = useState<FamilyMember[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchFamilyMembers = async () => {
      try {
        const members = await getAllFamilyMembers();
        setFamilyMembers(members);
        if (onLoaded) {
          onLoaded(members);
        }
      } catch (err) {
        console.error('Error fetching family members:', err);
        setError('Failed to load family members. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchFamilyMembers();
  }, [onLoaded]);

  if (loading) {
    return (
      <div className="mb-4 bg-white rounded-lg p-4 shadow-sm h-64 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto mb-2"></div>
          <p>Loading family members...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mb-4 bg-white rounded-lg p-4 shadow-sm">
        <div className="text-red-500 text-center">
          <p>{error}</p>
          <button 
            className="mt-2 px-4 py-2 bg-blue-500 text-white rounded-md"
            onClick={() => window.location.reload()}
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <section className="mb-4 bg-white rounded-lg p-4 shadow-sm">
      <h2 className="text-lg font-semibold mb-3">Jenny&apos;s Loved Ones</h2>
      <div className="flex gap-3 overflow-x-auto pb-2" style={{ scrollbarWidth: 'thin' }}>
        {familyMembers.map((member) => (
          <div key={member.id} className="flex-none w-[200px]">
            <div className="relative rounded-lg overflow-hidden">
              <div className="relative aspect-[4/5]">
                {/* Handle base64 encoded image */}
                <div 
                  className="w-full h-full bg-cover bg-center" 
                  style={{ 
                    backgroundImage: `url(data:image/jpeg;base64,${member.image})` 
                  }}
                />
                {member.isAdmin && (
                  <span className="absolute top-2 left-2 z-10 bg-[#6B6B6B] text-white px-2 py-0.5 text-xs rounded-full">
                    Admin
                  </span>
                )}
                <div 
                  className={`absolute bottom-2 left-2 right-2 p-3 rounded-lg ${member.color === '#FFD400' ? 'text-black' : 'text-white'}`}
                  style={{ backgroundColor: member.color }}
                >
                  <h3 className="text-base font-bold">{member.name}</h3>
                  <p className={`text-xs ${member.color === '#FFD400' ? 'text-black/90' : 'text-white/90'}`}>{member.relationship}</p>
                  <Link 
                    href={`/family?name=${encodeURIComponent(member.name)}`}
                    className={`absolute right-3 top-1/2 -translate-y-1/2 ${member.color === '#FFD400' ? 'text-black/70 hover:text-black' : 'text-white/70 hover:text-white'}`}
                    aria-label="View details"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" className="rotate-90">
                      <g fill="currentColor">
                        <path d="m14.829 11.948l1.414-1.414L12 6.29l-4.243 4.243l1.415 1.414L11 10.12v7.537h2V10.12z"/>
                        <path fillRule="evenodd" d="M19.778 4.222c-4.296-4.296-11.26-4.296-15.556 0s-4.296 11.26 0 15.556s11.26 4.296 15.556 0s4.296-11.26 0-15.556m-1.414 1.414A9 9 0 1 0 5.636 18.364A9 9 0 0 0 18.364 5.636" clipRule="evenodd"/>
                      </g>
                    </svg>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        ))}
        <div className="flex-none w-[200px]">
          <div className="border-2 border-dashed rounded-lg flex items-center justify-center aspect-[4/5] hover:bg-gray-50 cursor-pointer transition-colors">
            <div className="text-center">
              <div className="text-2xl mb-1 text-gray-400">+</div>
              <span className="text-sm text-gray-600">Add People</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
} 