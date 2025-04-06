import React, { useState, useEffect } from 'react';
import { View, Text, Image, StyleSheet, ScrollView, Dimensions, Pressable } from 'react-native';
import { useLocalSearchParams, router } from 'expo-router';
import * as FileSystem from 'expo-file-system';
import LeftArrow from '../assets/components/LeftArrow';
import GreenPlay from '../assets/components/GreenPlay';
import DanielIcons from '../assets/components/DanielIcons';
import MichelleIcons from '../assets/components/MichelleIcons';

const { width } = Dimensions.get('window');

export default function ProfilePage() {
  const { name } = useLocalSearchParams();
  const [imageCache, setImageCache] = useState<{ [key: string]: string }>({});
  const [isImageLoaded, setIsImageLoaded] = useState(false);
  
  const profileInfo = {
    'Daniel': {
      fullName: 'Daniel Kim',
      relation: "Your Grandson",
      nicknames: 'Danny, Dan',
      audioAlbums: [
        { title: "We need to talk soon! Maybe", addedTime: '2 hrs ago' },
        { title: 'Grandma, how are you? Are you', addedTime: '5 days ago' }
      ],
      photoAlbums: [
        require('../assets/images/album1.png'),
        require('../assets/images/album2.png'),
        require('../assets/images/album3.png')
      ],
      image: require('../assets/images/daniel.png'),
      IconComponent: DanielIcons
    },
    'Michelle': {
      fullName: 'Michelle Feng',
      relation: "Your Granddaughter",
      nicknames: 'Mishy, Love',
      audioAlbums: [
        { title: "Let's go dancing soon! I miss", addedTime: '5 hrs ago' },
        { title: 'Hi Grandma! I love you mwah', addedTime: '3 days ago' }
      ],
      photoAlbums: [
        require('../assets/images/album4.png'),
        require('../assets/images/album5.png'),
        require('../assets/images/album6.png')
      ],
      image: require('../assets/images/michelle.png'),
      IconComponent: MichelleIcons
    }
  }[name as string];

  // Pre-load and cache images
  useEffect(() => {
    const cacheImages = async () => {
      if (!profileInfo) return;

      try {
        // Cache main profile image
        const mainAsset = Image.resolveAssetSource(profileInfo.image);
        const mainCacheKey = `${FileSystem.cacheDirectory}${name}_profile.jpg`;
        await FileSystem.downloadAsync(mainAsset.uri, mainCacheKey);
        
        // Cache album images
        const albumCache: { [key: string]: string } = {};
        for (let i = 0; i < profileInfo.photoAlbums.length; i++) {
          const asset = Image.resolveAssetSource(profileInfo.photoAlbums[i]);
          const cacheKey = `${FileSystem.cacheDirectory}${name}_album_${i}.jpg`;
          await FileSystem.downloadAsync(asset.uri, cacheKey);
          albumCache[`album_${i}`] = cacheKey;
        }

        setImageCache({ profile: mainCacheKey, ...albumCache });
        setIsImageLoaded(true);
      } catch (error) {
        console.error('Error caching images:', error);
        setIsImageLoaded(true); // Still set to true to show fallback images
      }
    };

    cacheImages();
  }, [name]);

  if (!profileInfo) {
    return (
      <View style={styles.container}>
        <Text>Profile not found</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView style={styles.scrollView}>
        <View style={styles.imageContainer}>
          <Image 
            source={imageCache.profile ? { uri: imageCache.profile } : profileInfo.image}
            style={styles.headerImage}
          />
          <Pressable 
            style={styles.backButton}
            onPress={() => router.back()}
          >
            <LeftArrow width={24} height={24} fill="#fff" />
          </Pressable>
        </View>

        <View style={styles.headerInfoContainer}>
          <View style={styles.headerTextContainer}>
            <Text style={styles.headerName}>{profileInfo.fullName}</Text>
            <Text style={styles.headerRelation}>{profileInfo.relation}</Text>
          </View>
          <View style={styles.headerIconsContainer}>
            {React.createElement(profileInfo.IconComponent)}
          </View>
        </View>

        <View style={styles.content}>
          {/* Basic Information */}
          <View style={styles.card}>
            <Text style={styles.cardTitle}>Basic Information</Text>
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Name:</Text>
              <Text style={styles.infoValue}>{profileInfo.fullName}</Text>
            </View>
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Relationship:</Text>
              <Text style={styles.infoValue}>{profileInfo.relation}</Text>
            </View>
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Nicknames:</Text>
              <Text style={styles.infoValue}>{profileInfo.nicknames}</Text>
            </View>
          </View>

          {/* Audio Albums */}
          <View style={styles.card}>
            <Text style={styles.cardTitle}>Audio Albums</Text>
            {profileInfo.audioAlbums.map((album, index) => (
              <View key={index} style={styles.audioItem}>
                <GreenPlay width={28} height={28} />
                <View style={styles.audioInfo}>
                  <Text style={styles.audioTitle}>{album.title}</Text>
                  <Text style={styles.audioTime}>Added {album.addedTime}</Text>
                </View>
              </View>
            ))}
          </View>

          {/* Photo Albums */}
          <View style={styles.card}>
            <Text style={styles.cardTitle}>Photo Albums</Text>
            <View style={styles.photoGrid}>
              {profileInfo.photoAlbums.map((photo, index) => (
                <Image 
                  key={index} 
                  source={imageCache[`album_${index}`] ? { uri: imageCache[`album_${index}`] } : photo}
                  style={styles.photoItem} 
                />
              ))}
            </View>
          </View>

          {/* Recent Albums */}
          <View style={styles.card}>
            <Text style={styles.cardTitle}>Recent Albums</Text>
            <View style={styles.photoGrid}>
              {profileInfo.photoAlbums.map((photo, index) => (
                <Image 
                  key={index} 
                  source={imageCache[`album_${index}`] ? { uri: imageCache[`album_${index}`] } : photo}
                  style={styles.photoItem} 
                />
              ))}
            </View>
          </View>
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9F4F2',
  },
  scrollView: {
    flex: 1,
  },
  imageContainer: {
    position: 'relative',
    width: width,
    height: width,
  },
  headerImage: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
  },
  headerInfoContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 24,
    paddingVertical: 16,
  },
  headerTextContainer: {
    flex: 1,
  },
  headerName: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#000000',
  },
  headerRelation: {
    fontSize: 16,
    color: '#666666',
    marginTop: 4,
  },
  headerIconsContainer: {
    marginLeft: 16,
  },
  backButton: {
    position: 'absolute',
    top: 60,
    left: 20,
    padding: 8,
    zIndex: 2,
  },
  content: {
    padding: 20,
  },
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 20,
    marginBottom: 16,
    shadowColor: '#000000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  cardTitle: {
    fontSize: 18,
    marginBottom: 16,
  },
  infoRow: {
    flexDirection: 'row',
    marginBottom: 8,
  },
  infoLabel: {
    width: 100,
    fontSize: 16,
    color: '#666666',
  },
  infoValue: {
    flex: 1,
    fontWeight: 'bold',
    fontSize: 16,
  },
  audioItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  audioInfo: {
    marginLeft: 12,
    flex: 1,
  },
  audioTitle: {
    fontSize: 16,
    marginBottom: 4,
    fontWeight: 'bold',
  },
  audioTime: {
    fontSize: 14,
    color: '#666666',
  },
  photoGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  photoItem: {
    width: (width - 64) / 3,
    height: (width - 64) / 3,
    borderRadius: 8,
  },
}); 