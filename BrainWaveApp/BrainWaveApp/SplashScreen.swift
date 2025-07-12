//
//  SplashScreen.swift
//  BrainWaveApp
//
//  Created by Chandler Ketelsen on 7/12/25.
//

import SwiftUI

struct SplashScreen: View {
    @EnvironmentObject var appState: AppState
    @State private var displayedText = ""
    @State private var fullText = "BrainWave Analytics"
    @State private var currentIndex = 0
    @State private var showCursor = true
    
    var body: some View {
        ZStack {
            // Background gradient
            LinearGradient(
                gradient: Gradient(colors: [
                    Color(red: 0.1, green: 0.1, blue: 0.2),
                    Color(red: 0.05, green: 0.05, blue: 0.1)
                ]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
            
            VStack(spacing: 30) {
                // App icon placeholder
                Image(systemName: "brain.head.profile")
                    .font(.system(size: 80))
                    .foregroundColor(.blue)
                    .scaleEffect(1.2)
                
                // Terminal typing effect
                HStack(spacing: 0) {
                    Text(displayedText)
                        .font(.system(size: 32, weight: .bold, design: .monospaced))
                        .foregroundColor(.green)
                    
                    if showCursor {
                        Rectangle()
                            .fill(Color.green)
                            .frame(width: 2, height: 32)
                            .animation(.easeInOut(duration: 0.5).repeatForever(autoreverses: true), value: showCursor)
                    }
                }
                
                // Subtitle
                Text("Parking Lot Analytics Platform")
                    .font(.system(size: 18, weight: .medium))
                    .foregroundColor(.gray)
                    .opacity(displayedText.count == fullText.count ? 1 : 0)
                    .animation(.easeInOut(duration: 0.5).delay(0.5), value: displayedText.count)
            }
        }
        .onAppear {
            startTypingEffect()
        }
    }
    
    private func startTypingEffect() {
        Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { timer in
            if currentIndex < fullText.count {
                let index = fullText.index(fullText.startIndex, offsetBy: currentIndex)
                displayedText += String(fullText[index])
                currentIndex += 1
            } else {
                timer.invalidate()
                // Wait a bit then transition to login
                DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
                    appState.transitionToLogin()
                }
            }
        }
    }
}

#Preview {
    SplashScreen()
        .environmentObject(AppState())
} 
