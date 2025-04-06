interface RobotIconProps {
  className?: string;
}

export function RobotIcon({ className = "" }: RobotIconProps) {
  return (
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      width="24" 
      height="24" 
      viewBox="0 0 24 24"
      className={className}
    >
      <g 
        fill="none" 
        stroke="currentColor" 
        strokeLinecap="round" 
        strokeLinejoin="round" 
        strokeWidth="1.5" 
        color="currentColor"
      >
        <path d="M19 16v-2c0-2.828 0-4.243-.879-5.121C17.243 8 15.828 8 13 8h-2c-2.828 0-4.243 0-5.121.879C5 9.757 5 11.172 5 14v2c0 2.828 0 4.243.879 5.121C6.757 22 8.172 22 11 22h2c2.828 0 4.243 0 5.121-.879C19 20.243 19 18.828 19 16m0 2c1.414 0 2.121 0 2.56-.44c.44-.439.44-1.146.44-2.56s0-2.121-.44-2.56C21.122 12 20.415 12 19 12M5 18c-1.414 0-2.121 0-2.56-.44C2 17.122 2 16.415 2 15s0-2.121.44-2.56C2.878 12 3.585 12 5 12m8.5-8.5a1.5 1.5 0 1 1-3 0a1.5 1.5 0 0 1 3 0M12 5v3m-3 5v1m6-1v1" />
        <path d="M10 17.5s.667.5 2 .5s2-.5 2-.5" />
      </g>
    </svg>
  );
} 