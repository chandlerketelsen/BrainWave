//
//  AppCoordinator.swift
//  BrainWaveApp
//
//  Created by Chandler Ketelsen on 7/12/25.
//

import SwiftUI

struct AppCoordinator: View {
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        Group {
            switch appState.currentScreen {
            case .splash:
                SplashScreen()
            case .login:
                LoginScreen()
            case .tutorial:
                TutorialScreen()
            case .home:
                HomeScreen()
            }
        }
        .animation(.easeInOut(duration: 0.5), value: appState.currentScreen)
    }
}

#Preview {
    AppCoordinator()
        .environmentObject(AppState())
} 