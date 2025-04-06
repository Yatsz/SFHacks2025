'use client';

import Image from 'next/image';
import { useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { getAllFamilyMembers } from '@/lib/firebase/services/familyService';

interface FamilyMemberData {
  name: string;
  relationship: string;
  nicknames: string[];
  audioMessages: {
    title: string;
    addedTime: string;
  }[];
  reminders: {
    message: string;
    requestedBy: string;
  }[];
  image: string;
}

const getMemberIdByName = (name: string): string => {
  switch (name) {
    case "Michelle Feng":
      return "member1";
    case "Daniel Kim":
      return "member2";
    default:
      return "member1";
  }
};

const familyData: Record<string, FamilyMemberData> = {
  "member1": {
    name: "Michelle Feng",
    relationship: "Jenny's Granddaughter",
    nicknames: ["Mishy", "Love"],
    audioMessages: [
      { title: "Let's go dancing soon! I miss you Grandma", addedTime: "3 hrs ago" },
      { title: "Hi Grandma! I love you mwah mwah", addedTime: "3 days ago" }
    ],
    reminders: [
      { message: "Reminder for her to attend brunch April 7 at 12pm", requestedBy: "Daniel" },
      { message: "Reminder for her to wash her hair next Monday", requestedBy: "Lia" }
    ],
    image: ""
  },
  "member2": {
    name: "Daniel Kim",
    relationship: "Jenny's Grandson",
    nicknames: ["Dan", "Danny"],
    audioMessages: [
      { title: "Grandma, remember to take your medicine!", addedTime: "1 hr ago" },
      { title: "I'll visit you this weekend!", addedTime: "2 days ago" }
    ],
    reminders: [
      { message: "Reminder to take evening medication", requestedBy: "Michelle" },
      { message: "Doctor's appointment next Tuesday", requestedBy: "Daniel" }
    ],
    image: ""
  }
};

export default function FamilyProfile() {
  const searchParams = useSearchParams();
  const name = searchParams.get('name');
  const memberId = name ? getMemberIdByName(name) : 'member1';
  const [member, setMember] = useState(familyData[memberId]);

  useEffect(() => {
    const fetchMemberData = async () => {
      try {
        const members = await getAllFamilyMembers();
        const currentMember = members.find(m => m.name === name);
        if (currentMember) {
          setMember({
            ...familyData[memberId],
            image: currentMember.image || ''
          });
        }
      } catch (error) {
        console.error('Error fetching member data:', error);
      }
    };

    fetchMemberData();
  }, [name, memberId]);

  if (!member) {
    return <div>Member not found</div>;
  }

  return (
    <div className="min-h-screen px-[70px]" style={{ backgroundColor: '#F9F4F2' }}>
      {/* Banner Container */}
      <div className="relative w-full h-[225px]">
        {/* Banner Image Container */}
        <div className="absolute inset-0 rounded-t-[10px] overflow-hidden z-0">
          <Image
            src={memberId === 'member1' ? '/bg1.png' : '/bg2.png'}
            alt="Banner"
            fill
            className="object-cover"
          />
        </div>
        {/* Profile Picture and Info */}
        <div className="absolute -bottom-[90px] left-[70px] z-10 flex items-end gap-6">
          {/* Profile Picture */}
          {member.image ? (
            <div 
              className="w-[140px] h-[140px] rounded-[10px] bg-cover bg-center shadow-md"
              style={{ 
                backgroundImage: `url(data:image/jpeg;base64,${member.image})`,
                backgroundPosition: '50% 30%'
              }}
            />
          ) : (
            <div className="w-[140px] h-[140px] rounded-[10px] shadow-md bg-gray-200 flex items-center justify-center">
              <span className="text-2xl font-semibold text-gray-600">
                {member.name.split(' ').map(n => n[0]).join('')}
              </span>
            </div>
          )}
          
          {/* Name and Relationship */}
          <div className="flex items-end gap-4 pb-4">
            <div>
              <h1 className="text-2xl font-bold text-black mb-1">{member.name}</h1>
              <p className="text-gray-600">{member.relationship}</p>
            </div>
            <Image src="/speaker.svg" alt="Speaker" width={24} height={24} className="mb-1" />
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="px-[70px] mt-[110px]">
        <div className="flex items-center justify-end mb-4">
          <span className="text-gray-600">Admin</span>
        </div>

        <div className="grid grid-cols-12 gap-8">
          {/* Left Column */}
          <div className="col-span-4">
            <div className="bg-white rounded-lg p-6 mb-6 shadow-[0_2px_8px_rgba(0,0,0,0.1)] min-h-[280px]">
              <h2 className="text-lg font-semibold mb-2">Basic Information</h2>
              <p className="text-sm text-gray-500 mb-4">This section is about you</p>
              
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-gray-500">Name:</p>
                  <p className="font-medium">{member.name}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Relationship:</p>
                  <p className="font-medium">{member.relationship}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Nicknames:</p>
                  <p className="font-medium">{member.nicknames.join(", ")}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-[0_2px_8px_rgba(0,0,0,0.1)]">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold">Photo Album</h2>
                <button className="text-sm px-4 py-1 bg-gray-100 rounded-full">+ Add</button>
              </div>
              <div className="grid grid-cols-3 gap-2">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="aspect-square relative">
                    <Image
                      src={memberId === 'member1' ? `/sample${i}.png` : `/sample${i + 3}.png`}
                      alt={`Photo ${i}`}
                      fill
                      className="object-cover rounded-lg"
                    />
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Middle Column */}
          <div className="col-span-4">
            <div className="bg-white rounded-lg p-6 mb-6 shadow-[0_2px_8px_rgba(0,0,0,0.1)] min-h-[280px] flex flex-col">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold">Audio Album</h2>
                <button className="text-sm px-4 py-1 bg-gray-100 rounded-full">+ Add</button>
              </div>
              <div className="space-y-3 flex-grow">
                {member.audioMessages.map((message, index) => (
                  <div key={index} className="flex items-center gap-3 bg-gray-50 p-3 rounded-lg">
                    <Image src="/play.svg" alt="Play" width={24} height={24} />
                    <div>
                      <p className="text-sm font-medium">{message.title}</p>
                      <p className="text-xs text-gray-500">Added {message.addedTime}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-[0_2px_8px_rgba(0,0,0,0.1)]">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold">Recent Album</h2>
                <button className="text-sm px-4 py-1 bg-gray-100 rounded-full">+ Add</button>
              </div>
              <div className="grid grid-cols-3 gap-2">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="aspect-square relative">
                    <Image
                      src={memberId === 'member1' ? `/sample${i}.png` : `/sample${i + 3}.png`}
                      alt={`Recent Photo ${i}`}
                      fill
                      className="object-cover rounded-lg"
                    />
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column */}
          <div className="col-span-4">
            <div className="bg-white rounded-lg p-6 shadow-[0_2px_8px_rgba(0,0,0,0.1)]">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold">Routine & Reminders</h2>
                <p className="text-sm text-gray-500">Approve new routines & reminders as admin</p>
              </div>
              <div className="space-y-3">
                {member.reminders.map((reminder, index) => (
                  <div key={index} className="flex items-center justify-between bg-gray-50 px-2 py-3 rounded-lg">
                    <div>
                      <p className="text-sm">{reminder.message}</p>
                      <p className="text-xs text-gray-500">Requested by {reminder.requestedBy}</p>
                    </div>
                    <div className="flex gap-2">
                      <Image src="/no.svg" alt="Decline" width={24} height={24} className="cursor-pointer" />
                      <Image src="/yes.svg" alt="Accept" width={24} height={24} className="cursor-pointer" />
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-4 flex gap-2">
                <input
                  type="text"
                  placeholder="Message"
                  className="flex-1 border rounded-full px-4 py-2 text-sm"
                />
                <button className="px-6 py-2 bg-[#8CD7F3] text-black rounded-full text-sm">
                  Add
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}