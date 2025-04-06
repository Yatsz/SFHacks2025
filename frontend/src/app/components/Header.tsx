'use client';

import { RobotIcon } from './RobotIcon';
import { BellIcon } from './BellIcon';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Header() {
  const pathname = usePathname();

  const isActive = (path: string) => {
    return pathname === path;
  };

  return (
    <nav className="flex items-center justify-between px-8 py-3" style={{ backgroundColor: '#F9F4F2' }}>
      <div className="flex items-center gap-2">
        <Link href="/" className="text-xl font-semibold flex items-center gap-2">
          <RobotIcon className="w-6 h-6" /> Remi
        </Link>
        <div className="flex gap-6 ml-8">
          <Link 
            href="/memory-bank" 
            className={isActive('/memory-bank') ? 'border-b-2 border-black' : ''}
          >
            Memory Bank
          </Link>
          <Link 
            href="/schedule"
            className={isActive('/schedule') ? 'border-b-2 border-black' : ''}
          >
            Schedule
          </Link>
          <Link 
            href="/robot-status"
            className={isActive('/robot-status') ? 'border-b-2 border-black' : ''}
          >
            Robot Status
          </Link>
          <Link 
            href="/summary"
            className={isActive('/summary') ? 'border-b-2 border-black' : ''}
          >
            Summary
          </Link>
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
  );
} 