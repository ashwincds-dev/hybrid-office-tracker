#!/bin/bash
# Quick test script to check if teammates can access your app

echo "🧪 Testing Office Tracker Access"
echo "================================"
echo ""

# Get network IP
echo "📍 Your Network IP:"
IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
echo "   $IP"
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
    exit 1
fi
echo ""

# Test network IP
echo "🌐 Testing network access..."
if curl -s http://$IP:5000/health > /dev/null 2>&1; then
    echo "   ✅ Network access works"
    echo ""
    echo "   Share this URL with your team:"
    echo "   📱 http://$IP:5000"
else
    echo "   ⚠️  Network access might be blocked"
    echo ""
    echo "   Possible issues:"
    echo "   1. Firewall blocking port 5000"
    echo "   2. Network restrictions"
    echo ""
    echo "   Fix: Allow Python through firewall"
    echo "   Run: sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add \$(which python3)"
fi
echo ""

# Check firewall
echo "🔥 Firewall status..."
if /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate | grep -q "enabled"; then
    echo "   ⚠️  Firewall is ENABLED"
    echo "   May need to allow Python through firewall"
else
    echo "   ✅ Firewall is disabled"
fi
echo ""

# Show health status
echo "💊 Application health..."
HEALTH=$(curl -s http://localhost:5000/health)
if [ ! -z "$HEALTH" ]; then
    echo "   ✅ Healthy"
    echo "   $HEALTH"
else
    echo "   ❌ Health check failed"
fi
echo ""

# Summary
echo "================================"
echo "📋 Summary:"
echo ""
echo "Your URL: http://$IP:5000"
echo ""
echo "Next steps:"
echo "1. Share URL with teammates"
echo "2. Have them open in browser"
echo "3. They should click 'Register'"
echo ""
echo "If teammates can't access:"
echo "→ Run: sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add \$(which python3)"
echo "→ Or see: QUICK_TEAM_SETUP.md"
echo ""

