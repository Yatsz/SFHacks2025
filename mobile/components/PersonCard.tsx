import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

interface PersonCardProps {
  name: string;
  relation: string;
}

export default function PersonCard({ name, relation }: PersonCardProps) {
  return (
    <View style={styles.container}>
      <View style={styles.textContainer}>
        <Text style={styles.name}>{name}</Text>
        <Text style={styles.relation}>{relation}</Text>
      </View>
      <TouchableOpacity style={styles.button}>
        <Text style={styles.buttonText}>Listen to Voice</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.profileButton}>
        <Text style={styles.profileButtonText}>View full profile</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    alignItems: 'center',
  },
  textContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  relation: {
    fontSize: 16,
    color: '#666',
  },
  button: {
    backgroundColor: '#4CAF50',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 20,
    marginBottom: 10,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
  },
  profileButton: {
    paddingHorizontal: 20,
    paddingVertical: 10,
  },
  profileButtonText: {
    color: '#666',
    fontSize: 14,
  },
}); 