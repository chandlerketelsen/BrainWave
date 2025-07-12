//
//  TutorialScreen.swift
//  BrainWaveApp
//
//  Created by Chandler Ketelsen on 7/12/25.
//

import SwiftUI

struct TutorialScreen: View {
    @EnvironmentObject var appState: AppState
    @State private var currentPage = 0
    
    private let tutorialPages = [
        TutorialPage(
            title: "Welcome to BrainWave",
            subtitle: "Your Drone Analytics Platform",
            description: "Transform raw drone footage into actionable insights with our advanced AI-powered analytics platform.",
            imageName: "brain.head.profile",
            backgroundColor: Color(red: 0.1, green: 0.2, blue: 0.3)
        ),
        TutorialPage(
            title: "Real-time Monitoring",
            subtitle: "Parking Lot Analytics",
            description: "Monitor parking occupancy, predict future trends, and optimize space utilization with real-time data from your drones.",
            imageName: "car.fill",
            backgroundColor: Color(red: 0.2, green: 0.1, blue: 0.3)
        )
    ]
    
    var body: some View {
        ZStack {
            // Background gradient
            LinearGradient(
                gradient: Gradient(colors: [
                    tutorialPages[currentPage].backgroundColor,
                    tutorialPages[currentPage].backgroundColor.opacity(0.7)
                ]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
            
            VStack(spacing: 0) {
                // Page content
                TabView(selection: $currentPage) {
                    ForEach(0..<tutorialPages.count, id: \.self) { index in
                        TutorialPageView(page: tutorialPages[index])
                            .tag(index)
                    }
                }
                .tabViewStyle(PageTabViewStyle(indexDisplayMode: .never))
                .animation(.easeInOut(duration: 0.3), value: currentPage)
                
                // Bottom controls
                VStack(spacing: 20) {
                    // Page indicators
                    HStack(spacing: 8) {
                        ForEach(0..<tutorialPages.count, id: \.self) { index in
                            Circle()
                                .fill(index == currentPage ? Color.white : Color.white.opacity(0.3))
                                .frame(width: 8, height: 8)
                                .animation(.easeInOut(duration: 0.3), value: currentPage)
                        }
                    }
                    
                    // Navigation buttons
                    HStack(spacing: 20) {
                        if currentPage > 0 {
                            Button("Back") {
                                withAnimation {
                                    currentPage -= 1
                                }
                            }
                            .foregroundColor(.white)
                            .padding(.horizontal, 30)
                            .padding(.vertical, 12)
                            .background(Color.white.opacity(0.2))
                            .cornerRadius(25)
                        }
                        
                        Spacer()
                        
                        Button(currentPage == tutorialPages.count - 1 ? "Get Started" : "Next") {
                            if currentPage == tutorialPages.count - 1 {
                                appState.transitionToHome()
                            } else {
                                withAnimation {
                                    currentPage += 1
                                }
                            }
                        }
                        .foregroundColor(.white)
                        .padding(.horizontal, 30)
                        .padding(.vertical, 12)
                        .background(Color.blue)
                        .cornerRadius(25)
                    }
                    .padding(.horizontal, 40)
                }
                .padding(.bottom, 50)
            }
        }
    }
}

struct TutorialPage {
    let title: String
    let subtitle: String
    let description: String
    let imageName: String
    let backgroundColor: Color
}

struct TutorialPageView: View {
    let page: TutorialPage
    
    var body: some View {
        VStack(spacing: 40) {
            Spacer()
            
            // Icon
            Image(systemName: page.imageName)
                .font(.system(size: 100))
                .foregroundColor(.white)
                .scaleEffect(1.2)
            
            // Text content
            VStack(spacing: 20) {
                Text(page.title)
                    .font(.system(size: 32, weight: .bold))
                    .foregroundColor(.white)
                    .multilineTextAlignment(.center)
                
                Text(page.subtitle)
                    .font(.system(size: 20, weight: .medium))
                    .foregroundColor(.white.opacity(0.8))
                    .multilineTextAlignment(.center)
                
                Text(page.description)
                    .font(.system(size: 16))
                    .foregroundColor(.white.opacity(0.7))
                    .multilineTextAlignment(.center)
                    .lineLimit(nil)
                    .padding(.horizontal, 40)
            }
            
            Spacer()
        }
        .padding(.horizontal, 20)
    }
}

#Preview {
    TutorialScreen()
        .environmentObject(AppState())
} 