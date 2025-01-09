import * as React from "react";
import Svg, { Rect, Text } from "react-native-svg";
const SVGComponent = (props) => (
  <Svg
    width={400}
    height={200}
    viewBox="0 0 400 200"
    xmlns="http://www.w3.org/2000/svg"
    {...props}
  >
    <Rect x={0} y={0} width={400} height={200} fill="#bfbfbf" />
    <Rect x={0} y={180} width={400} height={20} fill="#d3d3d3" />
    <Rect x={50} y={160} width={300} height={20} fill="#0e8381" />
    <Text x={200} y={195} fontSize={10} textAnchor="middle" fill="#000000">
      {"\n    SiO\u2082\n  "}
    </Text>
    <Text x={200} y={175} fontSize={10} textAnchor="middle" fill="#ffffff">
      {"\n    BE\n  "}
    </Text>
    <Rect x={50} y={140} width={60} height={20} fill="#1E90FF" />
    <Rect x={50} y={120} width={60} height={20} fill="#FFA500" />
    <Rect x={50} y={100} width={60} height={20} fill="#1E90FF" />
    <Rect x={170} y={140} width={60} height={20} fill="#1E90FF" />
    <Rect x={170} y={120} width={60} height={20} fill="#FFA500" />
    <Rect x={170} y={100} width={60} height={20} fill="#1E90FF" />
    <Rect x={290} y={140} width={60} height={20} fill="#1E90FF" />
    <Rect x={290} y={120} width={60} height={20} fill="#FFA500" />
    <Rect x={290} y={100} width={60} height={20} fill="#1E90FF" />
    <Rect
      x={0}
      y={100}
      width={50}
      height={80}
      fill="#8c8c8c"
      fillOpacity={0.3}
    />
    <Rect
      x={110}
      y={100}
      width={60}
      height={60}
      fill="#8c8c8c"
      fillOpacity={0.3}
    />
    <Rect
      x={230}
      y={100}
      width={60}
      height={60}
      fill="#8c8c8c"
      fillOpacity={0.3}
    />
    <Rect
      x={350}
      y={100}
      width={50}
      height={80}
      fill="#8c8c8c"
      fillOpacity={0.3}
    />
    <Rect x={30} y={40} width={90} height={60} fill="#FFD700" />
    <Rect x={160} y={40} width={80} height={60} fill="#FFD700" />
    <Rect x={280} y={40} width={90} height={60} fill="#FFD700" />
    <Text x={200} y={75} fontSize={10} textAnchor="middle" fill="#000000">
      {"\n    TE\n  "}
    </Text>
    <Text x={200} y={20} fontSize={12} textAnchor="middle" fill="#000000">
      {"\n    Step 10: Device Ready (After Lift-Off)\n  "}
    </Text>
  </Svg>
);
export default SVGComponent;
