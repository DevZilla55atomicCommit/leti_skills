#!/bin/bash
# Verify that App.tsx imports React Navigation components
if grep -q "import { NavigationContainer }" App.tsx && \
   grep -q "import { createNativeStackNavigator }" App.tsx; then
  echo "✅ React Navigation imports found in App.tsx"
  exit 0
else
  echo "❌ React Navigation imports missing in App.tsx"
  exit 1
fi