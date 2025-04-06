import React, { useState, useEffect, useRef } from 'react';
import { View, StyleSheet, Dimensions, Button, Text, Image, ImageSourcePropType, Pressable } from 'react-native';
import { CameraView, useCameraPermissions, CameraType } from 'expo-camera';
import * as ImageManipulator from 'expo-image-manipulator';
import { router } from 'expo-router';
import Animated, { 
  useSharedValue, 
  useAnimatedStyle, 
  withSpring,
  interpolate,
  useAnimatedGestureHandler,
  runOnJS,
  withTiming,
  Easing
} from 'react-native-reanimated';
import { PanGestureHandler } from 'react-native-gesture-handler';
import * as FileSystem from 'expo-file-system';
import { SvgXml } from 'react-native-svg';
import DanielIcons from '../assets/components/DanielIcons';
import MichelleIcons from '../assets/components/MichelleIcons';
import Play from '../assets/components/Play';
import { MaterialIcons } from '@expo/vector-icons';
import Remi from '../assets/components/Remi';

const { width, height } = Dimensions.get('window');
const SHEET_HEIGHT = height * 0.45; // 40% of screen height
const SWIPE_THRESHOLD = 50;
const CAPTURE_INTERVAL = 2000; // Reduce to 2 seconds
const IMAGE_QUALITY = 0.4; // Reduce quality for faster processing
const RESIZE_WIDTH = 480; // Smaller resize width for faster processing

// Animation config for smoother performance
const SPRING_CONFIG = {
  damping: 15,
  mass: 1,
  stiffness: 100,
};

const TIMING_CONFIG = {
  duration: 250,
  easing: Easing.bezier(0.25, 0.1, 0.25, 1),
};

interface DetectedPerson {
  name: string;
  similarity: number;
  relation: string;
}

interface ProfileInfo {
  fullName: string;
  relation: string;
  image: ImageSourcePropType;
  IconComponent: React.ComponentType<any>;
}

interface ProfileData {
  [key: string]: ProfileInfo;
}

const profileData: ProfileData = {
  'Daniel': {
    fullName: 'Daniel Kim',
    relation: 'Your Grandson',
    image: require('../assets/images/daniel-half.png'),
    IconComponent: DanielIcons
  },
  'Michelle': {
    fullName: 'Michelle Feng',
    relation: 'Your Granddaughter',
    image: require('../assets/images/michelle-half.png'),
    IconComponent: MichelleIcons
  }
};

export default function App() {
  const [permission, requestPermission] = useCameraPermissions();
  const [cameraType, setCameraType] = useState<CameraType>('front');
  const [detectedPerson, setDetectedPerson] = useState<DetectedPerson | null>(null);
  const [isCardVisible, setIsCardVisible] = useState(false);
  const cameraRef = useRef<CameraView>(null);
  const slideUp = useSharedValue(0);
  const lastDetectionTime = useRef<{ [key: string]: number }>({});
  const [imageCache, setImageCache] = useState<{ [key: string]: string }>({});

  // Pre-load and cache images
  useEffect(() => {
    const cacheImages = async () => {
      const cache: { [key: string]: string } = {};
      for (const [name, profile] of Object.entries(profileData)) {
        try {
          const asset = Image.resolveAssetSource(profile.image);
          const cacheKey = `${FileSystem.cacheDirectory}${name}.jpg`;
          await FileSystem.downloadAsync(asset.uri, cacheKey);
          cache[name] = cacheKey;
        } catch (error) {
          console.error('Error caching image:', error);
        }
      }
      setImageCache(cache);
    };
    cacheImages();
  }, []);

  // Animation styles
  const overlayStyle = useAnimatedStyle(() => {
    return {
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.5)',
      opacity: withTiming(
        interpolate(slideUp.value, [0, 1], [0, 0.5]),
        TIMING_CONFIG
      )
    };
  });

  const bottomSheetStyle = useAnimatedStyle(() => {
    return {
      position: 'absolute',
      bottom: 0,
      left: 0,
      right: 0,
      height: SHEET_HEIGHT,
      backgroundColor: 'white',
      borderTopLeftRadius: 20,
      borderTopRightRadius: 20,
      transform: [{
        translateY: withSpring(
          interpolate(slideUp.value, [0, 1], [SHEET_HEIGHT, 0]),
          SPRING_CONFIG
        )
      }]
    };
  });

  const gestureHandler = useAnimatedGestureHandler({
    onStart: (_, context: any) => {
      context.startY = slideUp.value;
    },
    onActive: (event, context) => {
      const newValue = context.startY + event.translationY / SHEET_HEIGHT;
      slideUp.value = Math.max(0, Math.min(1, newValue));
    },
    onEnd: (event) => {
      if (event.translationY > SWIPE_THRESHOLD) {
        slideUp.value = withSpring(0);
        runOnJS(setIsCardVisible)(false);
        runOnJS(setDetectedPerson)(null);
      } else {
        slideUp.value = withSpring(1);
      }
    },
  });

  useEffect(() => {
    const interval = setInterval(captureAndSendFrame, CAPTURE_INTERVAL);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (detectedPerson && !isCardVisible) {
      slideUp.value = withSpring(1);
      setIsCardVisible(true);
    }
  }, [detectedPerson]);

  const canShowPerson = (personName: string): boolean => {
    const now = Date.now();
    const lastTime = lastDetectionTime.current[personName] || 0;
    return now - lastTime > 30000; // 30 seconds cooldown
  };

  const captureAndSendFrame = async () => {
    if (cameraRef.current) {
      
        const photo = await cameraRef.current.takePictureAsync({
          quality: IMAGE_QUALITY,
          skipProcessing: true,
          shutterSound: false,
          imageType: 'jpg'
        });
        if (!photo) return;
        
        const resizedPhoto = await ImageManipulator.manipulateAsync(
          photo.uri,
          [{ resize: { width: RESIZE_WIDTH } }],
          { base64: true, format: ImageManipulator.SaveFormat.JPEG, compress: IMAGE_QUALITY }
        );

        const response = await fetch('http://localhost:8000/detect', {  
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            image: resizedPhoto.base64
          })
        });

        const result = await response.json();
        if (result.persons && result.persons.length > 0 && 
            result.persons[0].similarity > 0.6 && 
            canShowPerson(result.persons[0].name)) {
          setDetectedPerson(result.persons[0]);
          lastDetectionTime.current[result.persons[0].name] = Date.now();
        }
      
    }
  };

  const navigateToProfile = (name: string) => {
    router.push(`/profile?name=${name}`);
  };

  const toggleCameraType = () => {
    setCameraType(current => current === 'front' ? 'back' : 'front');
  };

  if (!permission) {
    return <View style={styles.container} />;
  }

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Button onPress={requestPermission} title="Grant Permission" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <CameraView
        ref={cameraRef}
        style={styles.camera}
        facing={cameraType}
        enableTorch={false}
        flash="off"
        videoStabilizationMode="auto"
        animateShutter={false}
      />
      <View style={styles.logoContainer}>
        <Remi width={120} height={40} />
      </View>
      <Pressable 
        style={styles.switchCameraButton}
        onPress={toggleCameraType}
      >
        <MaterialIcons name="flip-camera-ios" size={20} color="white" />
      </Pressable>
      <Animated.View style={overlayStyle} pointerEvents={isCardVisible ? 'auto' : 'none'} />
      <PanGestureHandler onGestureEvent={gestureHandler}>
        <Animated.View style={bottomSheetStyle}>
          {detectedPerson && profileData[detectedPerson.name] && (
            <View style={styles.cardContainer}>
              <Image 
                source={imageCache[detectedPerson.name] ? { uri: imageCache[detectedPerson.name] } : profileData[detectedPerson.name].image}
                style={styles.headerImage}
              />
              <View style={styles.pullBar} />
              <View style={styles.contentContainer}>
                <View style={styles.leftContent}>
                  <Text style={styles.nameText}>
                    {profileData[detectedPerson.name].fullName}
                  </Text>
                  <Text style={styles.relationText}>
                    {profileData[detectedPerson.name].relation}
                  </Text>
                  <View style={styles.iconsContainer}>
                    {React.createElement(profileData[detectedPerson.name].IconComponent)}
                  </View>
                </View>
                <View style={styles.rightContent}>
                  <Pressable 
                    style={styles.listenButton}
                    onPress={() => {/* TODO: Implement voice playback */}}
                  >
                    <Play width={20} height={20} fill="#fff" style={styles.playIcon} />
                    <Text style={styles.listenButtonText}>Listen to Voice</Text>
                  </Pressable>
                  <Pressable 
                    style={styles.profileButton}
                    onPress={() => navigateToProfile(detectedPerson.name)}
                  >
                    <Text style={styles.profileButtonText}>View full profile</Text>
                  </Pressable>
                </View>
              </View>
            </View>
          )}
        </Animated.View>
      </PanGestureHandler>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  camera: {
    width,
    height,
  },
  cardContainer: {
    width: '100%',
    position: 'relative',
  },
  headerImage: {
    width: '100%',
    height: width * 0.6,
    resizeMode: 'cover',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
  },
  pullBar: {
    width: 40,
    height: 4,
    backgroundColor: '#D9D9D9',
    borderRadius: 2,
    position: 'absolute',
    top: 10,
    alignSelf: 'center',
    zIndex: 1,
  },
  contentContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 16,
    paddingTop: 20,
  },
  leftContent: {
    flex: 1,
    marginRight: 16,
  },
  rightContent: {
    alignItems: 'flex-end',
    gap: 8,
  },
  nameText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#000',
  },
  relationText: {
    fontSize: 16,
    color: '#666',
    marginTop: 4,
  },
  listenButton: {
    backgroundColor: '#4CAF50',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  listenButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  profileButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  profileButtonText: {
    color: '#000',
    fontSize: 14,
  },
  iconsContainer: {
    marginTop: 8,
  },
  playIcon: {
    marginRight: 4,
  },
  switchCameraButton: {
    position: 'absolute',
    top: 88,
    right: 30,
    borderRadius: 25,
    padding: 8,
    zIndex: 2,
  },
  logoContainer: {
    position: 'absolute',
    top: 95,
    left: 30,
    right: 0,
    alignItems: 'center',
    zIndex: 2,
  },
}); 