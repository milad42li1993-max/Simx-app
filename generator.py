import os

def write(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

write("settings.gradle.kts", """
pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories { google(); mavenCentral() }
}
rootProject.name = "SIMX"
include(":app")
""")

write("build.gradle.kts", """
plugins {
    id("com.android.application") version "8.2.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.22" apply false
}
""")

write("gradle.properties", """
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
""")

write("app/build.gradle.kts", """
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}
android {
    namespace = "com.simx.app"
    compileSdk = 34
    defaultConfig {
        applicationId = "com.simx.app"
        minSdk = 26
        targetSdk = 34
        versionCode = 7
        versionName = "5.2.0"
    }
    buildTypes {
        release { isMinifyEnabled = false }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
    buildFeatures { compose = true }
    composeOptions { kotlinCompilerExtensionVersion = "1.5.8" }
    packaging {
        resources { excludes += "/META-INF/{AL2.0,LGPL2.1}" }
    }
}
dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    implementation("androidx.activity:activity-compose:1.8.2")
    implementation(platform("androidx.compose:compose-bom:2024.02.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.material3:material3")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
}
""")

write("app/src/main/AndroidManifest.xml", """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <application
        android:allowBackup="true"
        android:label="SIMX"
        android:supportsRtl="true"
        android:theme="@style/Theme.SIMX"
        android:usesCleartextTraffic="true">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
""")

write("app/src/main/res/values/strings.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">SIMX</string>
</resources>
""")

write("app/src/main/res/values/themes.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.SIMX" parent="android:Theme.Material.NoActionBar">
        <item name="android:statusBarColor">#060312</item>
        <item name="android:navigationBarColor">#060312</item>
        <item name="android:windowBackground">#060312</item>
    </style>
</resources>
""")

write("app/src/main/java/com/simx/app/MainActivity.kt", r'''
package com.simx.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import kotlin.math.cos
import kotlin.math.sin
import kotlin.random.Random

val Bg = Color(0xFF060312)
val CardBg = Color(0xFF120B26)
val BorderC = Color(0xFF2A1B54)
val Purple = Color(0xFFA855F7)
val Gold = Color(0xFFF3C623)
val Green = Color(0xFF00E676)
val Red = Color(0xFFFF3D00)
val White = Color(0xFFFAFAFA)
val Gray = Color(0xFF948EA5)

data class Candle(val o: Float, val h: Float, val l: Float, val c: Float)

data class Asset(
    val cat: String,
    val symbol: String,
    val name: String,
    var price: Float,
    var change: Float,
    val bias: String,
    val conf: Int,
    val story: String,
    val action: String,
    val entry: String,
    val sl: String,
    val tp: String,
    val rr: String,
    val candles: List<Candle>,
    val scores: List<Float>
)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { App() }
    }
}

@Composable
fun App() {
    var tab by remember { mutableIntStateOf(0) }
    var market by remember { mutableIntStateOf(0) }
    var idx by remember { mutableIntStateOf(0) }

    val assets = remember {
        mutableStateListOf(
            Asset("crypto", "BTC/USDT", "Bitcoin", 67820f, 3.85f, "Bullish Strong", 88,
                "Order Flow shows aggressive buy absorption. Liquidity pool above is the next magnet.",
                "LONG", "67100-67400", "66150", "69800", "1:2.4",
                genCandles(true), listOf(0.9f, 0.85f, 0.95f, 0.7f, 0.88f)),
            Asset("crypto", "ETH/USDT", "Ethereum", 3540f, 2.40f, "Bullish", 79,
                "Price structure aligned on 4H with rising L2 activity. Trend remains constructive.",
                "LONG", "3490-3510", "3420", "3680", "1:2.1",
                genCandles(true), listOf(0.8f, 0.75f, 0.85f, 0.65f, 0.8f)),
            Asset("crypto", "SOL/USDT", "Solana", 148.5f, 9.20f, "Bullish Strong", 91,
                "Institutional capital flow detected. Sellers exited and expansion phase is likely.",
                "LONG", "144-146", "138", "162", "1:2.7",
                genCandles(true), listOf(0.95f, 0.9f, 0.9f, 0.85f, 0.92f)),
            Asset("crypto", "BNB/USDT", "BNB", 588f, -0.90f, "Range", 52,
                "Price rejected near resistance. Wait for clear structure shift before entry.",
                "WAIT", "-", "-", "-", "-",
                genCandles(false), listOf(0.4f, 0.5f, 0.3f, 0.6f, 0.45f)),
            Asset("crypto", "XRP/USDT", "XRP", 0.625f, 0.30f, "Compression", 58,
                "Volatility compression is extreme. A breakout move is statistically near.",
                "WAIT", "-", "-", "-", "-",
                genCandles(true), listOf(0.5f, 0.6f, 0.55f, 0.9f, 0.5f)),
            Asset("crypto", "ADA/USDT", "Cardano", 0.445f, -3.10f, "Bearish", 74,
                "Bearish BOS confirmed with negative delta divergence. Downside continuation favored.",
                "SHORT", "0.452-0.458", "0.472", "0.395", "1:2.2",
                genCandles(false), listOf(0.2f, 0.3f, 0.15f, 0.4f, 0.25f)),
            Asset("forex", "XAU/USD", "Gold", 2348.80f, 1.12f, "Event Risk", 55,
                "Gold is near highs into US CPI. High-impact macro event risk remains elevated.",
                "WAIT", "-", "-", "-", "-",
                genCandles(true), listOf(0.6f, 0.7f, 0.4f, 0.95f, 0.65f)),
            Asset("forex", "EUR/USD", "EURUSD", 1.0818f, -0.55f, "Bearish", 76,
                "DXY strength is pressuring EUR. 4H LH-LL structure remains intact.",
                "SHORT", "1.0835-1.0850", "1.0890", "1.0740", "1:2.0",
                genCandles(false), listOf(0.3f, 0.25f, 0.2f, 0.5f, 0.3f)),
            Asset("forex", "GBP/USD", "GBPUSD", 1.2635f, -0.15f, "Neutral", 49,
                "Price is trapped between supply and demand. Fusion layer prefers no trade.",
                "WAIT", "-", "-", "-", "-",
                genCandles(false), listOf(0.5f, 0.45f, 0.5f, 0.4f, 0.48f))
        )
    }

    LaunchedEffect(Unit) {
        while (true) {
            delay(1200)
            for (i in assets.indices) {
                val a = assets[i]
                val d = (Random.nextFloat() - 0.48f) * (a.price * 0.0008f)
                a.price += d
                assets[i] = a.copy()
            }
        }
    }

    val list = assets.filter { if (market == 0) it.cat == "crypto" else it.cat == "forex" }
    if (idx >= list.size) idx = 0

    Column(Modifier.fillMaxSize().background(Bg)) {
        // Header
        Row(
            Modifier.fillMaxWidth().padding(horizontal = 20.dp, vertical = 14.dp),
            Arrangement.SpaceBetween,
            Alignment.CenterVertically
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(
                    Modifier.size(42.dp).clip(CircleShape)
                        .background(Brush.radialGradient(listOf(Gold.copy(alpha = 0.35f), Color.Transparent))),
                    contentAlignment = Alignment.Center
                ) { Text("SI", color = Gold, fontWeight = FontWeight.Black, fontSize = 16.sp) }
                Spacer(Modifier.width(10.dp))
                Column {
                    Text("SIMX", color = Gold, fontSize = 22.sp, fontWeight = FontWeight.Black)
                    Text("AI OPERATING SYSTEM", color = Purple, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                }
            }
            Surface(
                color = CardBg,
                shape = RoundedCornerShape(20.dp),
                modifier = Modifier.border(1.dp, BorderC, RoundedCornerShape(20.dp))
            ) {
                Row(Modifier.padding(horizontal = 12.dp, vertical = 6.dp), verticalAlignment = Alignment.CenterVertically) {
                    Box(Modifier.size(8.dp).clip(CircleShape).background(Green))
                    Spacer(Modifier.width(6.dp))
                    Text("21 Sensors Live", color = White, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                }
            }
        }

        // Market switch
        Row(
            Modifier.fillMaxWidth().padding(horizontal = 20.dp)
                .clip(RoundedCornerShape(14.dp)).background(CardBg)
                .border(1.dp, BorderC, RoundedCornerShape(14.dp)).padding(4.dp)
        ) {
            Box(
                Modifier.weight(1f).clip(RoundedCornerShape(10.dp))
                    .background(if (market == 0) Purple else Color.Transparent)
                    .clickable { market = 0; idx = 0 }
                    .padding(vertical = 10.dp),
                contentAlignment = Alignment.Center
            ) { Text("Crypto", color = White, fontWeight = FontWeight.Bold, fontSize = 13.sp) }

            Box(
                Modifier.weight(1f).clip(RoundedCornerShape(10.dp))
                    .background(if (market == 1) Purple else Color.Transparent)
                    .clickable { market = 1; idx = 0 }
                    .padding(vertical = 10.dp),
                contentAlignment = Alignment.Center
            ) { Text("Forex & Gold", color = White, fontWeight = FontWeight.Bold, fontSize = 13.sp) }
        }

        // Symbols
        LazyRow(
            Modifier.padding(vertical = 12.dp),
            contentPadding = PaddingValues(horizontal = 20.dp),
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            items(list.size) { i ->
                val sel = i == idx
                Box(
                    Modifier.clip(RoundedCornerShape(16.dp))
                        .background(if (sel) Gold else CardBg)
                        .border(1.dp, if (sel) Gold else BorderC, RoundedCornerShape(16.dp))
                        .clickable { idx = i }
                        .padding(horizontal = 16.dp, vertical = 10.dp)
                ) {
                    Text(list[i].symbol, color = if (sel) Bg else White, fontSize = 13.sp, fontWeight = FontWeight.Black)
                }
            }
        }

        Box(Modifier.weight(1f).padding(horizontal = 20.dp)) {
            if (list.isNotEmpty()) {
                when (tab) {
                    0 -> Dashboard(list[idx])
                    1 -> CenterText("Macro Events Calendar")
                    2 -> CenterText("AI Assistant Chat")
                    3 -> CenterText("VIP Account & Plans")
                }
            }
        }

        Surface(
            color = CardBg,
            modifier = Modifier.fillMaxWidth().border(1.dp, BorderC, RoundedCornerShape(topStart = 20.dp, topEnd = 20.dp))
        ) {
            Row(Modifier.fillMaxWidth().padding(vertical = 12.dp), Arrangement.SpaceEvenly) {
                listOf("AI Desk", "Events", "Chat", "Account").forEachIndexed { i, label ->
                    Text(
                        label,
                        color = if (i == tab) Gold else Gray,
                        fontSize = 12.sp,
                        fontWeight = if (i == tab) FontWeight.Black else FontWeight.Normal,
                        modifier = Modifier.clickable { tab = i }
                    )
                }
            }
        }
    }
}

@Composable
fun CenterText(t: String) {
    Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Text(t, color = White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
    }
}

@Composable
fun Dashboard(a: Asset) {
    LazyColumn(verticalArrangement = Arrangement.spacedBy(16.dp)) {
        item {
            Card(
                colors = CardDefaults.cardColors(containerColor = CardBg),
                shape = RoundedCornerShape(24.dp),
                modifier = Modifier.border(1.dp, BorderC, RoundedCornerShape(24.dp))
            ) {
                Column(Modifier.padding(20.dp)) {
                    Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween, Alignment.CenterVertically) {
                        Column {
                            Text(a.name, color = White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                            Text(a.symbol, color = Gray, fontSize = 12.sp)
                        }
                        Column(horizontalAlignment = Alignment.End) {
                            val p = if (a.price > 10f) String.format("%.2f", a.price) else String.format("%.4f", a.price)
                            Text(p, color = White, fontSize = 22.sp, fontWeight = FontWeight.Black)
                            Text(
                                (if (a.change >= 0) "+" else "") + String.format("%.2f", a.change) + "%",
                                color = if (a.change >= 0) Green else Red,
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }

                    Spacer(Modifier.height(14.dp))
                    Text("Live Candlestick (4H)", color = Gray, fontSize = 11.sp)
                    Spacer(Modifier.height(6.dp))
                    CandleChart(a.candles)

                    Spacer(Modifier.height(16.dp))
                    Text("AI Sensor Radar", color = Gold, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    Spacer(Modifier.height(8.dp))
                    Radar(a.scores)

                    Spacer(Modifier.height(14.dp))
                    val bc = when {
                        a.bias.contains("Bull") -> Green
                        a.bias.contains("Bear") -> Red
                        else -> Gold
                    }
                    Surface(
                        color = bc.copy(alpha = 0.12f),
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier.border(1.dp, bc.copy(alpha = 0.3f), RoundedCornerShape(12.dp))
                    ) {
                        Text(
                            "AI Bias: " + a.bias + " | Confidence: " + a.conf + "%",
                            color = bc,
                            fontSize = 13.sp,
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.padding(horizontal = 14.dp, vertical = 8.dp)
                        )
                    }

                    Spacer(Modifier.height(12.dp))
                    Text("Market Narrative", color = Purple, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    Spacer(Modifier.height(4.dp))
                    Text(a.story, color = Gray, fontSize = 13.sp, lineHeight = 20.sp)
                }
            }
        }

        if (a.action != "WAIT") {
            item {
                Card(
                    colors = CardDefaults.cardColors(containerColor = CardBg),
                    shape = RoundedCornerShape(24.dp),
                    modifier = Modifier.border(1.dp, BorderC, RoundedCornerShape(24.dp))
                ) {
                    Column(Modifier.padding(20.dp)) {
                        val ac = if (a.action == "LONG") Green else Red
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(Modifier.size(10.dp).clip(CircleShape).background(ac))
                            Spacer(Modifier.width(8.dp))
                            Text("Signal: " + a.action, color = White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                        }
                        Spacer(Modifier.height(14.dp))
                        Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween) {
                            Column {
                                Text("Entry", color = Gray, fontSize = 11.sp)
                                Text(a.entry, color = White, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                            }
                            Column(horizontalAlignment = Alignment.End) {
                                Text("Stop Loss", color = Gray, fontSize = 11.sp)
                                Text(a.sl, color = Red, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                        Spacer(Modifier.height(10.dp))
                        Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween) {
                            Column {
                                Text("Take Profit", color = Gray, fontSize = 11.sp)
                                Text(a.tp, color = Green, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                            }
                            Column(horizontalAlignment = Alignment.End) {
                                Text("R:R", color = Gray, fontSize = 11.sp)
                                Text(a.rr, color = Gold, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                        Spacer(Modifier.height(16.dp))
                        Button(
                            onClick = {},
                            modifier = Modifier.fillMaxWidth().height(50.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = Gold),
                            shape = RoundedCornerShape(14.dp)
                        ) {
                            Text("Execute Trade", color = Bg, fontWeight = FontWeight.Black, fontSize = 14.sp)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun CandleChart(candles: List<Candle>) {
    Canvas(
        Modifier.fillMaxWidth().height(110.dp)
            .background(Color(0xFF09051B), RoundedCornerShape(12.dp))
            .padding(8.dp)
    ) {
        if (candles.isEmpty()) return@Canvas
        val w = size.width
        val h = size.height
        val minP = candles.minOf { it.l }
        val maxP = candles.maxOf { it.h }
        val range = if (maxP - minP == 0f) 1f else maxP - minP
        val slot = w / candles.size
        val cw = slot * 0.6f

        candles.forEachIndexed { i, cnd ->
            val x = i * slot + slot / 2f
            val up = cnd.c >= cnd.o
            val col = if (up) Green else Red
            val hy = h - ((cnd.h - minP) / range * h)
            val ly = h - ((cnd.l - minP) / range * h)
            val oy = h - ((cnd.o - minP) / range * h)
            val cy = h - ((cnd.c - minP) / range * h)
            drawLine(col, Offset(x, hy), Offset(x, ly), strokeWidth = 2f)
            val top = minOf(oy, cy)
            val bh = maxOf(kotlin.math.abs(oy - cy), 3f)
            drawRect(col, topLeft = Offset(x - cw / 2f, top), size = Size(cw, bh))
        }
    }
}

@Composable
fun Radar(scores: List<Float>) {
    Canvas(Modifier.fillMaxWidth().height(130.dp)) {
        val cx = size.width / 2f
        val cy = size.height / 2f
        val r = minOf(cx, cy) * 0.85f
        val n = 5

        for (ring in listOf(0.33f, 0.66f, 1.0f)) {
            val p = Path()
            for (i in 0 until n) {
                val ang = (i * 360.0 / n - 90.0) * Math.PI / 180.0
                val x = cx + (r * ring * cos(ang)).toFloat()
                val y = cy + (r * ring * sin(ang)).toFloat()
                if (i == 0) p.moveTo(x, y) else p.lineTo(x, y)
            }
            p.close()
            drawPath(p, BorderC, style = Stroke(1.5f))
        }

        val dp = Path()
        for (i in 0 until n) {
            val s = scores.getOrElse(i) { 0.5f }
            val ang = (i * 360.0 / n - 90.0) * Math.PI / 180.0
            val x = cx + (r * s * cos(ang)).toFloat()
            val y = cy + (r * s * sin(ang)).toFloat()
            if (i == 0) dp.moveTo(x, y) else dp.lineTo(x, y)
            drawCircle(Purple, 4f, Offset(x, y))
        }
        dp.close()
        drawPath(dp, Purple.copy(alpha = 0.30f))
        drawPath(dp, Purple, style = Stroke(3f))
    }
}

fun genCandles(up: Boolean): List<Candle> {
    val out = mutableListOf<Candle>()
    var p = 100f
    repeat(15) {
        val o = p
        val c = o + if (up) Random.nextFloat() * 4f - 1.5f else Random.nextFloat() * 4f - 2.8f
        val h = maxOf(o, c) + Random.nextFloat() * 2f
        val l = minOf(o, c) - Random.nextFloat() * 2f
        out.add(Candle(o, h, l, c))
        p = c
    }
    return out
}
''')

print("SIMX v5.2 stable build generated")
