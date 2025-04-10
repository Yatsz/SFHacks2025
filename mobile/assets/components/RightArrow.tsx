import * as React from "react";
import Svg, { Path } from "react-native-svg";
import type { SvgProps } from "react-native-svg";
const SvgRightArrow = (props: SvgProps) => (
  <Svg
    xmlns="http://www.w3.org/2000/svg"
    width={24}
    height={24}
    fill="none"
    {...props}
  >
    <Path
      fill="#fff"
      d="m12.052 14.829 1.414 1.414L17.71 12l-4.243-4.243-1.414 1.415L13.88 11H6.343v2h7.537z"
    />
    <Path
      fill="#fff"
      fillRule="evenodd"
      d="M19.778 19.778c4.296-4.296 4.296-11.26 0-15.556s-11.26-4.296-15.556 0-4.296 11.26 0 15.556 11.26 4.296 15.556 0m-1.414-1.414A9 9 0 1 0 5.636 5.636a9 9 0 0 0 12.728 12.728"
      clipRule="evenodd"
    />
  </Svg>
);
export default SvgRightArrow;
