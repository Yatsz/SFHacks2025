import Image, { StaticImageData } from 'next/image';
import { RobotIcon } from './components/RobotIcon';
import { BellIcon } from './components/BellIcon';
import image1 from '@/assets/image1.jpg';
import image2 from '@/assets/image2.jpg';
import image3 from '@/assets/image3.jpg';
import image4 from '@/assets/image4.jpg';

interface FamilyMember {
  name: string;
  role: string;
  image: string | StaticImageData;
  isAdmin?: boolean;
  color: string;
}

interface Reminder {
  time: string;
  task: string;
}

export default function Home() {
  const familyMembers: FamilyMember[] = [
    {
      name: "Cam Nafarrate",
      role: "Jenny's Husband",
      image: image1,
      isAdmin: true,
      color: "#FF8A1F"
    },
    {
      name: "Lin Nafarrate",
      role: "Jenny's Daughter",
      image: image2,
      color: "#06B0FF"
    },
    {
      name: "Max Nafarrate",
      role: "Jenny's Grandson",
      image: image3,
      color: "#00B05D"
    },
    {
      name: "Emma Nafarrate",
      role: "Jenny's Granddaughter",
      image: image4,
      color: "#FFD400"
    }
  ];

  const reminders: Reminder[] = [
    { time: "9:00 AM", task: "Remind her to take medication" },
    { time: "12:00 PM", task: "Play \"The Beatles\" music album" },
    { time: "3:00 PM", task: "Ask if she wants to fold laundry together" }
  ];

  const weeklyAlerts = [
    "Jenny was most confused at 3:00 PM.",
    "Jenny didn't recognize Max. Would you like to add a new photo of Max?",
    "Jenny has left the safe zone 3 times this week."
  ];

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#F9F4F2' }}>
      {/* Navigation */}
      <nav className="flex items-center justify-between px-8 py-3" style={{ backgroundColor: '#F9F4F2' }}>
        <div className="flex items-center gap-2">
          <span className="text-xl font-semibold flex items-center gap-2">
            <RobotIcon className="w-6 h-6" /> Remi
          </span>
          <div className="flex gap-6 ml-8">
            <span>Memory Bank</span>
            <span>Schedule</span>
            <span>Robot Status</span>
            <span>Summary</span>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <button 
            className="rounded-full flex items-center justify-center text-black"
            style={{ 
              backgroundColor: '#8CD7F3',
              width: '79px',
              paddingTop: '4px',
              paddingBottom: '4px'
            }}
          >
            <span className="flex items-center gap-1">
              <span>+</span>
              <span>Add</span>
            </span>
          </button>
          <button className="p-2">
            <BellIcon className="w-6 h-6" />
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <main className="px-8 pb-4 pt-6">
        {/* Welcome Section */}
        <div className="mb-4">
          <h1 className="text-xl">
            Welcome, <span className="font-bold">Jenny's Family</span>
          </h1>
          <p className="text-gray-600">How can we help?</p>
        </div>

        {/* Family Members Grid */}
        <section className="mb-4 bg-white rounded-lg p-4 shadow-sm">
          <h2 className="text-lg font-semibold mb-3">Jenny's Loved Ones</h2>
          <div className="flex gap-3 overflow-x-auto pb-2" style={{ scrollbarWidth: 'thin' }}>
            {familyMembers.map((member) => (
              <div key={member.name} className="flex-none w-[200px]">
                <div className="relative rounded-lg overflow-hidden">
                  <div className="relative aspect-[4/5]">
                    <Image
                      src={member.image}
                      alt={member.name}
                      fill
                      className="object-cover"
                      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 25vw"
                      priority={member.isAdmin}
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
                      <p className={`text-xs ${member.color === '#FFD400' ? 'text-black/90' : 'text-white/90'}`}>{member.role}</p>
                      <button 
                        className={`absolute right-3 top-1/2 -translate-y-1/2 ${member.color === '#FFD400' ? 'text-black/70 hover:text-black' : 'text-white/70 hover:text-white'}`}
                        aria-label="View details"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" className="rotate-90">
                          <g fill="currentColor">
                            <path d="m14.829 11.948l1.414-1.414L12 6.29l-4.243 4.243l1.415 1.414L11 10.12v7.537h2V10.12z"/>
                            <path fillRule="evenodd" d="M19.778 4.222c-4.296-4.296-11.26-4.296-15.556 0s-4.296 11.26 0 15.556s11.26 4.296 15.556 0s4.296-11.26 0-15.556m-1.414 1.414A9 9 0 1 0 5.636 18.364A9 9 0 0 0 18.364 5.636" clipRule="evenodd"/>
                          </g>
                        </svg>
                      </button>
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

        {/* Dashboard Grid */}
        <div className="grid grid-cols-12 gap-4">
          {/* Routines & Reminders */}
          <div className="col-span-5 bg-white rounded-lg p-4 shadow-sm">
            <div className="flex justify-between items-center mb-3">
              <h2 className="text-base font-semibold">Routine & Reminders</h2>
              <button className="text-xs px-6 py-1 bg-gray-100 rounded-full" style={{ width: '100px' }}>+ Add</button>
            </div>
            <div className="space-y-2">
              {reminders.map((reminder) => (
                <div key={reminder.time} className="p-3 rounded-lg flex items-center gap-3" style={{ backgroundColor: '#8CD7F3' }}>
                  <div className="font-semibold text-sm whitespace-nowrap">{reminder.time}</div>
                  <div className="text-sm">{reminder.task}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Robot Status */}
          <div className="col-span-4 bg-white rounded-lg p-4 shadow-sm">
            <div className="flex flex-col h-full">
              <h2 className="text-base font-semibold mb-3">Robot Status</h2>
              <div className="bg-gray-50 rounded-lg p-3 mb-3">
                <div className="flex items-center gap-2">
                  <span className="h-2 w-2 bg-green-500 rounded-full"></span>
                  <div className="flex items-center gap-2">
                    <RobotIcon className="w-6 h-6" />
                    <span className="font-medium text-sm">Online</span>
                  </div>
                  <div className="ml-auto text-sm">
                    <span>Annex 1</span>
                    <span className="ml-3">92%</span>
                  </div>
                </div>
              </div>
              <div className="text-white p-3 rounded-lg mb-3 flex items-center gap-2 text-sm" style={{ backgroundColor: '#FF3434' }}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 9V14M12 16V16.01M5.07183 19H18.9282C20.4678 19 21.4301 17.3333 20.6603 16L13.7321 4C12.9623 2.66667 11.0378 2.66667 10.268 4L3.33978 16C2.56998 17.3333 3.53223 19 5.07183 19Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                Alert: Remi is moving outside of safe zone!
              </div>
              <div className="flex gap-2 mt-auto">
                <input
                  type="text"
                  placeholder="Message"
                  className="flex-1 border rounded-full px-3 py-1.5 text-sm"
                />
                <button className="px-4 py-1.5 bg-[#8CD7F3] text-black rounded-full text-sm">Send</button>
              </div>
            </div>
          </div>

          {/* Weekly Summary */}
          <div className="col-span-3 bg-white rounded-lg p-4 shadow-sm">
            <h2 className="text-base font-semibold mb-3">Weekly Summary</h2>
            <div className="space-y-2">
              {weeklyAlerts.map((alert, index) => (
                <div key={index} className="border rounded-lg p-2 text-sm">
                  {alert}
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
