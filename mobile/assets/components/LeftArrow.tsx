import * as React from "react";
import Svg, { Path } from "react-native-svg";
import type { SvgProps } from "react-native-svg";
const SvgLeftArrow = (props: SvgProps) => (
  <Svg
    xmlns="http://www.w3.org/2000/svg"
    width={24}
    height={24}
    fill="none"
    {...props}
  >
    <Path
      fill="#fff"
      d="m11.948 9.171-1.414-1.414L6.29 12l4.243 4.243 1.414-1.415L10.12 13h7.537v-2H10.12z"
    />
    <Path
      fill="#fff"
      fillRule="evenodd"
      d="M4.222 4.222c-4.296 4.296-4.296 11.26 0 15.556s11.26 4.296 15.556 0 4.296-11.26 0-15.556-11.26-4.296-15.556 0m1.414 1.414a9 9 0 1 0 12.728 12.728A9 9 0 0 0 5.636 5.636"
      clipRule="evenodd"
    />
  </Svg>
);
export default SvgLeftArrow;
