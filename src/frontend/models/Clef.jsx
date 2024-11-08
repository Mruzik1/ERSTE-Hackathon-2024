import React, { useRef, useEffect } from 'react';
import { useGLTF } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';

const Clef = (props) => {
  const group = useRef();

  const { nodes, materials } = useGLTF('/models/test_43.glb');

  const amplitude = 0.3;
  const frequency = 2;
  const amplitudeY = 0.45;
  const frequencyY = 3;
  let time = 0.01;

  const initialYPosition = useRef(0);

  useEffect(() => {
    if (group.current) {
      group.current.rotation.set(0, Math.PI, 0);
      initialYPosition.current = group.current.position.y;
    }
  }, [nodes]);

  useFrame((state, delta) => {
    if (group.current) {
      time += delta;
      const yPosition = amplitudeY * Math.sin(frequencyY * time);
      const angle = amplitude * Math.sin(frequency * time);

      group.current.position.y = initialYPosition.current + yPosition;
      group.current.rotation.y = angle + Math.PI;
    }
  });

  return (
    <group ref={group} {...props}  >
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Node1.geometry}
        onBeforeRender={() => nodes.Node1.geometry.center()}
      >
        <meshStandardMaterial
          color="#FF6347"  
          metalness={0.5}
          roughness={1}
        />
      </mesh>
    </group>
  );
};

export default Clef;

useGLTF.preload('/models/test_43.glb');
