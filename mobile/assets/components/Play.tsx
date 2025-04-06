import * as React from "react";
import Svg, { Path } from "react-native-svg";
import type { SvgProps } from "react-native-svg";
const SvgPlay = (props: SvgProps) => (
  <Svg
    xmlns="http://www.w3.org/2000/svg"
    width={20}
    height={20}
    fill="none"
    {...props}
  >
    <Path
      fill="#F9F4F2"
      d="M10 0a10 10 0 1 0 0 20 10 10 0 0 0 0-20M8 14.5v-9l6 4.5z"
    />
  </Svg>
);
export default SvgPlay;
