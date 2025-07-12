//
//  LoginScreen.swift
//  BrainWaveApp
//
//  Created by Chandler Ketelsen on 7/12/25.
//

import SwiftUI

struct LoginScreen: View {
    @EnvironmentObject var appState: AppState
    @State private var isLoading = false
    
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
            
            VStack(spacing: 40) {
                Spacer()
                
                // App branding
                VStack(spacing: 20) {
                    Image(systemName: "brain.head.profile")
                        .font(.system(size: 60))
                        .foregroundColor(.blue)
                    
                    Text("BrainWave Analytics")
                        .font(.system(size: 28, weight: .bold))
                        .foregroundColor(.white)
                    
                }
                
                Spacer()
                
                // Login buttons
                VStack(spacing: 16) {
                    // Google Sign In
                    Button(action: {
                        handleGoogleSignIn()
                    }) {
                        HStack {
                            Image(systemName: "globe")
                                .font(.system(size: 18))
                            Text("Continue with Google")
                                .font(.system(size: 16, weight: .medium))
                        }
                        .foregroundColor(.black)
                        .frame(maxWidth: .infinity)
                        .frame(height: 50)
                        .background(Color.white)
                        .cornerRadius(12)
                    }
                    .disabled(isLoading)
                    
                    // Apple Sign In
                    Button(action: {
                        handleAppleSignIn()
                    }) {
                        HStack {
                            Image(systemName: "applelogo")
                                .font(.system(size: 18))
                            Text("Continue with Apple")
                                .font(.system(size: 16, weight: .medium))
                        }
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .frame(height: 50)
                        .background(Color.black)
                        .cornerRadius(12)
                    }
                    .disabled(isLoading)
                    
                    // Demo Sign In
                    Button(action: {
                        handleDemoSignIn()
                    }) {
                        HStack {
                            Image(systemName: "play.fill")
                                .font(.system(size: 16))
                            Text("Try Demo")
                                .font(.system(size: 16, weight: .medium))
                        }
                        .foregroundColor(.blue)
                        .frame(maxWidth: .infinity)
                        .frame(height: 50)
                        .background(Color.blue.opacity(0.1))
                        .cornerRadius(12)
                        .overlay(
                            RoundedRectangle(cornerRadius: 12)
                                .stroke(Color.blue, lineWidth: 1)
                        )
                    }
                    .disabled(isLoading)
                }
                .padding(.horizontal, 40)
                
                Spacer()
                
                // Footer
                Text("By continuing, you agree to our Terms of Service and Privacy Policy")
                    .font(.system(size: 12))
                    .foregroundColor(.gray)
                    .multilineTextAlignment(.center)
                    .padding(.horizontal, 40)
                    .padding(.bottom, 20)
            }
        }
        .overlay(
            Group {
                if isLoading {
                    Color.black.opacity(0.4)
                        .ignoresSafeArea()
                    
                    ProgressView()
                        .scaleEffect(1.5)
                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                }
            }
        )
    }
    
    private func handleGoogleSignIn() {
        isLoading = true
        // Simulate Google sign in
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
            isLoading = false
            appState.isNewUser = false
            appState.loginUser()
        }
    }
    
    private func handleAppleSignIn() {
        isLoading = true
        // Simulate Apple sign in
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
            isLoading = false
            appState.isNewUser = false
            appState.loginUser()
        }
    }
    
    private func handleDemoSignIn() {
        isLoading = true
        // Simulate demo sign in
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
            isLoading = false
            appState.isNewUser = true
            appState.loginUser()
        }
    }
}

#Preview {
    LoginScreen()
        .environmentObject(AppState())
} 
