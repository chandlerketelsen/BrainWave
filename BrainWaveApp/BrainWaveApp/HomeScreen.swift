//
//  HomeScreen.swift
//  BrainWaveApp
//
//  Created by Chandler Ketelsen on 7/12/25.
//

import SwiftUI

struct HomeScreen: View {
    @EnvironmentObject var appState: AppState
    @StateObject private var parkingDataService = ParkingDataService()
    @State private var selectedTimeIndex = 24 // Current time (noon)
    @State private var showMenu = false
    @State private var showProfile = false
    
    private let timeSlots = Array(0...48) // 24 hours * 2 (30-minute intervals)
    
    var body: some View {
        ZStack {
            // Background
            Color(red: 0.05, green: 0.05, blue: 0.1)
                .ignoresSafeArea()
            
            VStack(spacing: 0) {
                // Top navigation bar
                HStack {
                    Button(action: {
                        showProfile.toggle()
                    }) {
                        Image(systemName: "person.circle.fill")
                            .font(.system(size: 30))
                            .foregroundColor(.white)
                    }
                    
                    Spacer()
                    
                    Text("BrainWave Analytics")
                        .font(.system(size: 20, weight: .bold))
                        .foregroundColor(.white)
                    
                    Spacer()
                    
                    Button(action: {
                        showMenu.toggle()
                    }) {
                        Image(systemName: "line.3.horizontal")
                            .font(.system(size: 24))
                            .foregroundColor(.white)
                    }
                }
                .padding(.horizontal, 20)
                .padding(.top, 10)
                .padding(.bottom, 20)
                
                // Main content area
                VStack(spacing: 20) {
                    // 3D Parking Lot Placeholder
                    ZStack {
                        RoundedRectangle(cornerRadius: 20)
                            .fill(
                                LinearGradient(
                                    gradient: Gradient(colors: [
                                        Color(red: 0.1, green: 0.1, blue: 0.2),
                                        Color(red: 0.05, green: 0.05, blue: 0.15)
                                    ]),
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                            )
                            .overlay(
                                RoundedRectangle(cornerRadius: 20)
                                    .stroke(Color.blue.opacity(0.3), lineWidth: 1)
                            )
                        
                        VStack(spacing: 15) {
                            // 3D effect placeholder
                            ZStack {
                                // Grid pattern for parking lot
                                VStack(spacing: 8) {
                                    ForEach(0..<6, id: \.self) { row in
                                        HStack(spacing: 8) {
                                            ForEach(0..<8, id: \.self) { col in
                                                Rectangle()
                                                    .fill(Color.gray.opacity(0.3))
                                                    .frame(width: 30, height: 20)
                                                    .cornerRadius(4)
                                            }
                                        }
                                    }
                                }
                                .rotation3DEffect(.degrees(15), axis: (x: 1, y: 0, z: 0))
                                .scaleEffect(0.8)
                                
                                // Overlay text
                            
                                Text("3D Parking Lot View")
                                        .font(.system(size: 18, weight: .bold))
                                        .foregroundColor(.white)
                                .padding(.top, 20)
                            }
                            
                            // Stats overlay
                            HStack(spacing: 20) {
                                StatCard(
                                    title: "Occupancy", 
                                    value: "\(Int(parkingDataService.parkingLots.first?.occupancyPercentage ?? 0))%", 
                                    color: .orange
                                )
                                StatCard(
                                    title: "Available", 
                                    value: "\(parkingDataService.parkingLots.first?.availableSpaces ?? 0)", 
                                    color: .green
                                )
                                StatCard(
                                    title: "Total", 
                                    value: "\(parkingDataService.parkingLots.first?.capacity ?? 0)", 
                                    color: .blue
                                )
                            }
                            .padding(.horizontal, 20)
                        }
                        .padding(30)
                    }
                    .frame(height: 400)
                    .padding(.horizontal, 20)
                    
                    // Time scroller
                    VStack(spacing: 10) {
                        Text("Time: \(formatTime(for: selectedTimeIndex))")
                            .font(.system(size: 16, weight: .medium))
                            .foregroundColor(.white)
                        
                        HStack(spacing: 0) {
                            // Time slider
                            Slider(
                                value: Binding(
                                    get: { Double(selectedTimeIndex) },
                                    set: { selectedTimeIndex = Int($0) }
                                ),
                                in: 0...48,
                                step: 1
                            )
                            .accentColor(.blue)
                            
                            // Time labels
                            HStack {
                                Text("00:00")
                                    .font(.system(size: 12))
                                    .foregroundColor(.gray)
                                
                                Spacer()
                                
                                Text("23:59")
                                    .font(.system(size: 12))
                                    .foregroundColor(.gray)
                            }
                            .padding(.horizontal, 10)
                        }
                    }
                    .padding(.horizontal, 20)
                    .padding(.vertical, 15)
                    .background(Color(red: 0.1, green: 0.1, blue: 0.15))
                    .cornerRadius(15)
                    .padding(.horizontal, 20)
                }
                
                Spacer()
            }
        }
        .sheet(isPresented: $showProfile) {
            ProfileView()
        }
        .sheet(isPresented: $showMenu) {
            MenuView()
        }
        .onAppear {
            Task {
                await parkingDataService.fetchParkingData()
            }
        }
    }
    
    private func formatTime(for index: Int) -> String {
        let hour = index / 2
        let minute = (index % 2) * 30
        return String(format: "%02d:%02d", hour, minute)
    }
}

struct StatCard: View {
    let title: String
    let value: String
    let color: Color
    
    var body: some View {
        VStack(spacing: 5) {
            Text(value)
                .font(.system(size: 20, weight: .bold))
                .foregroundColor(color)
            
            Text(title)
                .font(.system(size: 12))
                .foregroundColor(.gray)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 10)
        .background(Color(red: 0.1, green: 0.1, blue: 0.15))
        .cornerRadius(10)
    }
}

struct ProfileView: View {
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        NavigationView {
            VStack(spacing: 30) {
                Image(systemName: "person.circle.fill")
                    .font(.system(size: 80))
                    .foregroundColor(.blue)
                
                VStack(spacing: 10) {
                    Text("Demo User")
                        .font(.system(size: 24, weight: .bold))
                    
                    Text("demo@brainwave.com")
                        .font(.system(size: 16))
                        .foregroundColor(.gray)
                }
                
                Spacer()
            }
            .padding()
            .navigationTitle("Profile")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
        }
    }
}

struct MenuView: View {
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        NavigationView {
            List {
                Section("Analytics") {
                    MenuRow(icon: "chart.bar.fill", title: "Dashboard", color: .blue)
                    MenuRow(icon: "car.fill", title: "Parking Analytics", color: .green)
                    MenuRow(icon: "clock.fill", title: "Historical Data", color: .orange)
                }
                
                Section("Settings") {
                    MenuRow(icon: "gear", title: "Preferences", color: .gray)
                    MenuRow(icon: "questionmark.circle", title: "Help", color: .purple)
                    MenuRow(icon: "info.circle", title: "About", color: .blue)
                }
            }
            .navigationTitle("Menu")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
        }
    }
}

struct MenuRow: View {
    let icon: String
    let title: String
    let color: Color
    
    var body: some View {
        HStack {
            Image(systemName: icon)
                .foregroundColor(color)
                .frame(width: 20)
            
            Text(title)
            
            Spacer()
            
            Image(systemName: "chevron.right")
                .font(.system(size: 12))
                .foregroundColor(.gray)
        }
    }
}

#Preview {
    HomeScreen()
        .environmentObject(AppState())
} 
