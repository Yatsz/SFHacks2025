interface RobotIconProps {
  className?: string;
}

export function RobotIcon({ className }: RobotIconProps) {
  return (
    <svg
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <path
        d="M12 3C10.9 3 10 3.9 10 5V7H14V5C14 3.9 13.1 3 12 3M18 7H16V5C16 2.8 14.2 1 12 1C9.8 1 8 2.8 8 5V7H6C4.9 7 4 7.9 4 9V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V9C20 7.9 19.1 7 18 7M12 17C10.9 17 10 16.1 10 15C10 13.9 10.9 13 12 13C13.1 13 14 13.9 14 15C14 16.1 13.1 17 12 17Z"
        fill="currentColor"
      />
    </svg>
  );
} 