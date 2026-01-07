#!/bin/bash
# Test VPN access for Office Tracker

echo "🔐 Testing VPN Access for Office Tracker"
echo "========================================"
echo ""

# Get VPN IP
echo "📍 Finding your VPN IP..."
VPN_IP=$(ifconfig | grep -A 2 "utun" | grep "inet " | awk '{print $2}' | head -1)

if [ -z "$VPN_IP" ]; then
    echo "   ❌ No VPN connection found"
    echo "   Please connect to VPN first"
    exit 1
else
    echo "   ✅ VPN IP: $VPN_IP"
fi
echo ""

# Get WiFi IP
WIFI_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | grep -v "100.64" | awk '{print $2}' | head -1)
echo "📶 WiFi IP: $WIFI_IP"
echo ""

# Check if app is running
echo "🔍 Checking if app is running..."
if ps aux | grep -v grep | grep "python app.py" > /dev/null; then
    echo "   ✅ App is running"
else
    echo "   ❌ App is NOT running"
    echo "   Start it with: python app.py"
    exit 1
fi
echo ""

# Test localhost
echo "🏠 Testing localhost access..."
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "   ✅ Localhost works"
else
    echo "   ❌ Localhost failed"
fi
echo ""

# Test WiFi IP
echo "📶 Testing WiFi access..."
if curl -s --max-time 3 http://$WIFI_IP:5000/health > /dev/null 2>&1; then
    echo "   ✅ WiFi access works"
    echo "   📱 WiFi URL: http://$WIFI_IP:5000"
else
    echo "   ⚠️  WiFi access might be blocked"
fi
echo ""

# Test VPN IP
echo "🔐 Testing VPN access..."
if curl -s --max-time 5 http://$VPN_IP:5000/health > /dev/null 2>&1; then
    echo "   ✅ VPN access works! 🎉"
    echo ""
    echo "   Great news! Your app is accessible via VPN!"
    echo "   Share this URL with remote teammates:"
    echo "   📱 http://$VPN_IP:5000"
    echo ""
    echo "   Requirements:"
    echo "   - Teammates must be connected to company VPN"
    echo "   - Your Mac must stay on and connected"
else
    echo "   ❌ VPN access blocked"
    echo ""
    echo "   Your VPN likely blocks peer-to-peer connections."
    echo "   This is common with corporate VPNs."
    echo ""
    echo "   Solutions:"
    echo "   1. Contact IT to allow port 5000 on VPN"
    echo "   2. Deploy to cloud server (recommended)"
    echo "   3. Use ngrok for testing"
    echo ""
    echo "   See: VPN_ACCESS_GUIDE.md for full details"
fi
echo ""

# Summary
echo "========================================"
echo "📋 Summary:"
echo ""
echo "WiFi URL:  http://$WIFI_IP:5000 ✅"
echo "VPN URL:   http://$VPN_IP:5000 ⚠️ (test needed)"
echo ""
echo "Next step: Have a REMOTE teammate test:"
echo "1. Connect to VPN"
echo "2. Try: curl http://$VPN_IP:5000/health"
echo "3. Or open: http://$VPN_IP:5000 in browser"
echo ""
echo "If it works for them: Share VPN URL!"
echo "If it doesn't: Deploy to cloud (see TEAM_DEPLOYMENT_GUIDE.md)"
echo ""

