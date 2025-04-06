import Image from 'next/image';
import { RobotIcon } from '@/app/components/RobotIcon';
import Link from 'next/link';

export default function FamilyProfile() {
  return (
    <div className="min-h-screen bg-[#F9F4F2]">
      {/* Navigation */}
      <nav className="flex items-center justify-between px-8 py-4">
        <div className="flex items-center gap-8">
          <Link href="/" className="flex items-center gap-2">
            <RobotIcon className="w-6 h-6" />
            <span className="text-xl font-semibold">Remi</span>
          </Link>
          <div className="flex gap-8">
            <Link href="/memory-bank" className="border-b-2 border-black">Memory Bank</Link>
            <Link href="/schedule">Schedule</Link>
            <Link href="/robot-status">Robot Status</Link>
            <Link href="/summary">Summary</Link>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <button className="bg-[#8CD7F3] text-black px-4 py-1.5 rounded-full text-sm">
            + Add
          </button>
          <button>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M12 22C10.8954 22 10 21.1046 10 20H14C14 21.1046 13.1046 22 12 22ZM20 19H4V17L6 16V10.5C6 7.038 7.421 4.793 10 4.18V2H14V4.18C16.579 4.793 18 7.038 18 10.5V16L20 17V19Z" fill="currentColor"/>
            </svg>
          </button>
        </div>
      </nav>

      {/* Hero Banner */}
      <div className="mx-8 mt-4 rounded-2xl overflow-hidden">
        <div className="relative h-48 bg-gradient-to-r from-blue-200 to-pink-100">
          <Image
            src="/hero-background.jpg"
            alt="Background"
            fill
            className="object-cover mix-blend-overlay"
            priority
          />
        </div>
      </div>

      {/* Profile Section */}
      <div className="px-8">
        <div className="flex items-start -mt-16 mb-8">
          <div className="relative w-32 h-32 rounded-lg overflow-hidden border-4 border-white bg-white">
            <Image
              src="/cam-profile.jpg"
              alt="Cam Nafarrate"
              fill
              className="object-cover"
            />
          </div>
          <div className="ml-6 mt-16 flex items-center justify-between w-full">
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-semibold">Cam Nafarrate</h1>
              <button>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M3 18V12H7V18H3ZM10 18V6H14V18H10ZM17 18V10H21V18H17Z"/>
                </svg>
              </button>
            </div>
            <span className="bg-[#6B6B6B] text-white px-3 py-1 rounded-full text-sm">Admin</span>
          </div>
        </div>
        <p className="text-gray-600 mb-8">Jenny's Husband</p>

        {/* Content Grid */}
        <div className="grid grid-cols-2 gap-6">
          {/* Left Column */}
          <div className="space-y-6">
            {/* Basic Information */}
            <div className="bg-white rounded-lg p-6">
              <h2 className="text-lg font-semibold mb-1">Basic Information</h2>
              <p className="text-sm text-gray-500 mb-4">This section is about you</p>
              <div className="space-y-4">
                <div>
                  <p className="text-sm font-medium">Name:</p>
                  <p className="text-sm">Cam Nafarrate</p>
                </div>
                <div>
                  <p className="text-sm font-medium">Relationship:</p>
                  <p className="text-sm">Jenny's Husband</p>
                </div>
                <div>
                  <p className="text-sm font-medium">Nicknames:</p>
                  <p className="text-sm">Hubby, Honey</p>
                </div>
              </div>
            </div>

            {/* Photo Album */}
            <div className="bg-white rounded-lg p-6">
              <div className="flex justify-between items-center mb-1">
                <h2 className="text-lg font-semibold">Photo Album</h2>
                <button className="text-sm bg-[#8CD7F3] text-black px-4 py-1.5 rounded-full">+ Add</button>
              </div>
              <p className="text-sm text-gray-500 mb-4">Photo memories of you and Jenny</p>
              <div className="grid grid-cols-3 gap-2">
                <div className="aspect-square relative rounded-lg overflow-hidden">
                  <Image src="/photo1.jpg" alt="Memory 1" fill className="object-cover" />
                </div>
                <div className="aspect-square relative rounded-lg overflow-hidden">
                  <Image src="/photo2.jpg" alt="Memory 2" fill className="object-cover" />
                </div>
                <div className="aspect-square relative rounded-lg overflow-hidden">
                  <Image src="/photo3.jpg" alt="Memory 3" fill className="object-cover" />
                </div>
              </div>
            </div>
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            {/* Audio Album */}
            <div className="bg-white rounded-lg p-6">
              <div className="flex justify-between items-center mb-1">
                <h2 className="text-lg font-semibold">Audio Album</h2>
                <button className="text-sm bg-[#8CD7F3] text-black px-4 py-1.5 rounded-full">+ Add</button>
              </div>
              <p className="text-sm text-gray-500 mb-4">Record voice memos for Jenny</p>
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <button className="bg-[#8CD7F3] p-2 rounded-full">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M8 5V19L19 12L8 5Z"/>
                    </svg>
                  </button>
                  <div>
                    <p className="text-sm font-medium">Hi honey, did you enjoy your lunch today?</p>
                    <p className="text-xs text-gray-500">Added 5 hrs ago</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <button className="bg-[#8CD7F3] p-2 rounded-full">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M8 5V19L19 12L8 5Z"/>
                    </svg>
                  </button>
                  <div>
                    <p className="text-sm font-medium">Have an amazing morning brunch. I love you</p>
                    <p className="text-xs text-gray-500">Added 3 days ago</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Recent Album */}
            <div className="bg-white rounded-lg p-6">
              <div className="flex justify-between items-center mb-1">
                <h2 className="text-lg font-semibold">Recent Album</h2>
                <button className="text-sm bg-[#8CD7F3] text-black px-4 py-1.5 rounded-full">+ Add</button>
              </div>
              <p className="text-sm text-gray-500 mb-4">Recent photos of you and Jenny</p>
              <div className="grid grid-cols-3 gap-2">
                <div className="aspect-square relative rounded-lg overflow-hidden">
                  <Image src="/recent1.jpg" alt="Recent 1" fill className="object-cover" />
                </div>
                <div className="aspect-square relative rounded-lg overflow-hidden">
                  <Image src="/recent2.jpg" alt="Recent 2" fill className="object-cover" />
                </div>
                <div className="aspect-square relative rounded-lg overflow-hidden">
                  <Image src="/recent3.jpg" alt="Recent 3" fill className="object-cover" />
                </div>
              </div>
            </div>

            {/* Routine & Reminders */}
            <div className="bg-white rounded-lg p-6">
              <h2 className="text-lg font-semibold mb-1">Routine & Reminders</h2>
              <p className="text-sm text-gray-500 mb-4">Approve new routines & reminders as admin</p>
              <div className="space-y-3">
                <div className="flex items-center justify-between border rounded-lg p-3">
                  <div>
                    <p className="text-sm">Reminder for her to attend brunch April 7 at 12pm</p>
                    <p className="text-xs text-gray-500">Requested by Max</p>
                  </div>
                  <div className="flex gap-2">
                    <button className="text-red-500 hover:text-red-600">✕</button>
                    <button className="text-green-500 hover:text-green-600">✓</button>
                  </div>
                </div>
                <div className="flex items-center justify-between border rounded-lg p-3">
                  <div>
                    <p className="text-sm">Reminder for her to wash her hair next Monday</p>
                    <p className="text-xs text-gray-500">Requested by Emma</p>
                  </div>
                  <div className="flex gap-2">
                    <button className="text-red-500 hover:text-red-600">✕</button>
                    <button className="text-green-500 hover:text-green-600">✓</button>
                  </div>
                </div>
              </div>
              <div className="flex gap-2 mt-4">
                <input
                  type="text"
                  placeholder="Message"
                  className="flex-1 border rounded-full px-4 py-2 text-sm"
                />
                <button className="bg-[#8CD7F3] text-black px-4 py-2 rounded-full text-sm">
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