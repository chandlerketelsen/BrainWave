//
//  AppState.swift
//  BrainWaveApp
//
//  Created by Chandler Ketelsen on 7/12/25.
//

import SwiftUI

class AppState: ObservableObject {
    @Published var currentScreen: AppScreen = .splash
    @Published var isLoggedIn = false
    @Published var isNewUser = false
    @Published var userProfile: UserProfile?
    
    enum AppScreen {
        case splash
        case login
        case tutorial
        case home
    }
    
    func transitionToLogin() {
        withAnimation(.easeInOut(duration: 0.5)) {
            currentScreen = .login
        }
    }
    
    func transitionToTutorial() {
        withAnimation(.easeInOut(duration: 0.5)) {
            currentScreen = .tutorial
        }
    }
    
    func transitionToHome() {
        withAnimation(.easeInOut(duration: 0.5)) {
            currentScreen = .home
        }
    }
    
    func loginUser() {
        isLoggedIn = true
        if isNewUser {
            transitionToTutorial()
        } else {
            transitionToHome()
        }
    }
}

struct UserProfile {
    let id: String
    let name: String
    let email: String
    let profileImage: String?
} 