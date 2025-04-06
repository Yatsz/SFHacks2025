import * as React from "react";
import Svg, { Path } from "react-native-svg";
import type { SvgProps } from "react-native-svg";
const SvgGreenPlay = (props: SvgProps) => (
  <Svg
    xmlns="http://www.w3.org/2000/svg"
    width={27}
    height={27}
    fill="none"
    {...props}
  >
    <Path
      fill="#00B05D"
      d="M14 .667a13.333 13.333 0 1 0 0 26.666A13.333 13.333 0 0 0 14 .667M11.333 20V8l8 6z"
    />
  </Svg>
);
export default SvgGreenPlay;
