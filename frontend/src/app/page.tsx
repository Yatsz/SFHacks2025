import FamilyMembersClient from './components/FamilyMembersClient';

interface Reminder {
  time: string;
  task: string;
}

export default function Home() {
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
    <div className="px-[70px] pb-4 pt-6">
      {/* Welcome Section */}
      <div className="mb-4">
        <h1 className="text-xl">
          Welcome, <span className="font-bold">Jenny&apos;s Family</span>
        </h1>
        <p className="text-gray-600">How can we help?</p>
      </div>

      {/* Family Members Grid */}
      <FamilyMembersClient />

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
    </div>
  );
}
