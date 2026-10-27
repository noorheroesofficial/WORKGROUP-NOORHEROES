from pathlib import Path
base=Path('NoorHeroes/feature/feature-onboarding/src/commonMain/kotlin/com/noorheroes/feature/onboarding/ui')
p=base/'AddChildComponents.kt'
s=p.read_text(encoding='utf-8')
s=s.replace('import androidx.compose.foundation.layout.Arrangement', '''import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.selection.selectableGroup
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import androidx.compose.foundation.layout.Arrangement''')
start=s.index('    Row(\n',s.index('fun LearningLevelRow('))
end=s.index('\n@Composable\nfun LearningLevelCard',start)
s=s[:start]+'''    val titles = listOf(
        stringResource(Res.string.add_child_level_beginner_title),
        stringResource(Res.string.add_child_level_intermediate_title),
        stringResource(Res.string.add_child_level_advanced_title),
    )
    val subtitles = listOf(
        stringResource(Res.string.add_child_level_beginner_subtitle),
        stringResource(Res.string.add_child_level_intermediate_subtitle),
        stringResource(Res.string.add_child_level_advanced_subtitle),
    )
    val levels = listOf(LearningLevel.BEGINNER, LearningLevel.INTERMEDIATE, LearningLevel.ADVANCED)
    val emojis = listOf("🌱", "🌿", "🌳")
    val fontScale = LocalDensity.current.fontScale
    BoxWithConstraints(modifier.selectableGroup()) {
        if (maxWidth < 330.dp || fontScale > 1.2f) {
            Column(verticalArrangement = Arrangement.spacedBy(NoorHeroesTheme.spacing.space8)) {
                levels.forEachIndexed { i, level ->
                    LearningLevelCard(titles[i], subtitles[i], emojis[i], selectedLevel == level,
                        { onLevelSelected(level) }, Modifier.fillMaxWidth())
                }
            }
        } else {
            Row(Modifier.height(IntrinsicSize.Min), horizontalArrangement = Arrangement.spacedBy(NoorHeroesTheme.spacing.space8)) {
                levels.forEachIndexed { i, level ->
                    LearningLevelCard(titles[i], subtitles[i], emojis[i], selectedLevel == level,
                        { onLevelSelected(level) }, Modifier.weight(1f).fillMaxHeight())
                }
            }
        }
    }
}
''' + s[end:]
s=s.replace('.height(NoorHeroesTheme.sizes.cardMinHeight)', '.heightIn(min = NoorHeroesTheme.sizes.controlHeight)')
s=s.replace('.clickable(onClick = onClick)\n            .padding(vertical = NoorHeroesTheme.spacing.space12, horizontal = NoorHeroesTheme.spacing.space6)', '.selectable(selected = isSelected, role = Role.RadioButton, onClick = onClick)\n            .padding(NoorHeroesTheme.spacing.space12)')
s=s.replace('                maxLines = 1,\n','').replace('                maxLines = 2,\n                overflow = TextOverflow.Ellipsis,\n','')
s+='''
/** Consistent semantic heading; icon is decorative because the label names the field. */
@Composable
internal fun ProfileSectionHeading(label: String, icon: ImageVector, modifier: Modifier = Modifier) {
    Row(modifier, verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(NoorHeroesTheme.spacing.space6)) {
        Icon(icon, contentDescription = null, tint = NoorHeroesTheme.colors.textSecondary,
            modifier = Modifier.size(18.dp))
        Text(label, style = NoorHeroesTheme.typography.enLabel.copy(fontWeight = FontWeight.SemiBold),
            color = NoorHeroesTheme.colors.textPrimary)
    }
}
'''
p.write_text(s,encoding='utf-8')
p=base/'AddChildScreen.kt';s=p.read_text(encoding='utf-8')
s=s.replace('import androidx.compose.foundation.background','''import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Person
import androidx.compose.material.icons.rounded.DateRange
import androidx.compose.material.icons.rounded.Face
import androidx.compose.material.icons.rounded.School
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.heightIn
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.unit.dp
import com.noorheroes.core.common.profile_multiple_children
import androidx.compose.foundation.background''')
s=s.replace('.noorHeroesSafeArea(),','.noorHeroesSafeArea()\n            .imePadding(),')
import re
for key,icon in [('nickname','Person'),('dob','DateRange'),('avatar','Face'),('learning_level','School')]:
    pattern=r'Text\(\s*text = stringResource\(Res.string.add_child_section_'+key+r'\),\s*style = NoorHeroesTheme.typography.enLabel.copy\(\s*fontWeight = FontWeight.Bold,\s*\),\s*color = NoorHeroesTheme.colors.textPrimary,\s*\)'
    s,n=re.subn(pattern,'ProfileSectionHeading(stringResource(Res.string.add_child_section_'+key+'), Icons.Rounded.'+icon+')',s)
    assert n==1,key
s=s.replace('OptionalPreferencesSection(\n                isExpanded = state.isOptionalExpanded,\n                onToggleExpand = onToggleOptionalSection,','ProfilePreferencesSections(')
needle='''            )
        }

        // Date Picker Modal Dialog'''
assert needle in s
s=s.replace(needle,'''            )
            Spacer(Modifier.height(NoorHeroesTheme.spacing.space8))
            androidx.compose.material3.TextButton(
                onClick = { focusManager.clearFocus(); onSubmit() },
                enabled = state.isSubmitEnabled && !state.isLoading,
                modifier = Modifier.align(Alignment.CenterHorizontally).heightIn(min = 48.dp),
            ) {
                Text(stringResource(Res.string.profile_multiple_children),
                    style = NoorHeroesTheme.typography.enCaption,
                    textDecoration = TextDecoration.Underline)
            }
        }

        // Date Picker Modal Dialog''')
p.write_text(s,encoding='utf-8')
p=base/'ChildPreferredLanguageSheet.kt';s=p.read_text(encoding='utf-8').replace('import androidx.compose.material.icons.Icons','import androidx.compose.material.icons.rounded.Language\nimport androidx.compose.material.icons.Icons')
s=s.replace('Text(stringResource(Res.string.child_preferred_language), style = NoorHeroesTheme.typography.enLabel,\n            color = NoorHeroesTheme.colors.textPrimary)','ProfileSectionHeading(stringResource(Res.string.child_preferred_language), Icons.Rounded.Language)')
p.write_text(s,encoding='utf-8')
p=base/'AddChildPreferencesComponents.kt';s=p.read_text(encoding='utf-8')
s=s.replace('import com.noorheroes.feature.onboarding.data.ChildInterestOption','''import com.noorheroes.feature.onboarding.data.ChildInterestOption
import com.noorheroes.feature.onboarding.data.AvatarCatalogRepositoryImpl
import com.noorheroes.feature.onboarding.data.profilePreferenceGroups
import com.noorheroes.core.common.profile_learning_focus
import com.noorheroes.core.common.profile_focus_quran
import com.noorheroes.core.common.profile_focus_stories
import com.noorheroes.core.common.profile_focus_arabic
import com.noorheroes.core.common.profile_focus_prayers
import com.noorheroes.core.common.profile_focus_values
import com.noorheroes.core.common.profile_interest_science
import com.noorheroes.core.common.profile_interest_arts''')
start=s.index('/**\n * Collapsible')
end=s.index('/**\n * Chip representing',start)
s=s[:start]+'''/** Inline sections backed by the established catalog; both serialize as interests. */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun ProfilePreferencesSections(
    selectedInterests: Set<String>, onToggleInterest: (String) -> Unit,
    dailyGoalMinutes: Int, onDailyGoalChanged: (Int) -> Unit,
    aiVoicePermission: Boolean, onAiVoiceToggled: (Boolean) -> Unit,
    modifier: Modifier = Modifier,
) {
    val labels = mapOf(
        "quran" to stringResource(Res.string.profile_focus_quran),
        "stories" to stringResource(Res.string.profile_focus_stories),
        "arabic" to stringResource(Res.string.profile_focus_arabic),
        "prayers" to stringResource(Res.string.profile_focus_prayers),
        "values" to stringResource(Res.string.profile_focus_values),
        "science" to stringResource(Res.string.profile_interest_science),
        "arts" to stringResource(Res.string.profile_interest_arts),
    )
    val groups = profilePreferenceGroups(AvatarCatalogRepositoryImpl().getAvailableInterests())
    Column(modifier, verticalArrangement = Arrangement.spacedBy(NoorHeroesTheme.spacing.space16)) {
        listOf(stringResource(Res.string.profile_learning_focus) to groups.learningFocus,
            stringResource(Res.string.add_child_interests_label) to groups.interests).forEach { (title, options) ->
            Column(verticalArrangement = Arrangement.spacedBy(NoorHeroesTheme.spacing.space8)) {
                Text(title, style = NoorHeroesTheme.typography.enLabel,
                    color = NoorHeroesTheme.colors.textPrimary)
                FlowRow(horizontalArrangement = Arrangement.spacedBy(NoorHeroesTheme.spacing.space8),
                    verticalArrangement = Arrangement.spacedBy(NoorHeroesTheme.spacing.space8)) {
                    options.forEach { option ->
                        InterestChip(option.copy(label = labels[option.id] ?: option.label),
                            option.id in selectedInterests, { onToggleInterest(option.id) })
                    }
                }
            }
        }
        Text(stringResource(Res.string.add_child_daily_goal_label), style = NoorHeroesTheme.typography.enLabel)
        FlowRow(horizontalArrangement = Arrangement.spacedBy(NoorHeroesTheme.spacing.space8),
            verticalArrangement = Arrangement.spacedBy(NoorHeroesTheme.spacing.space8)) {
            DAILY_GOAL_OPTIONS.forEach { minutes ->
                NoorChip(selected = dailyGoalMinutes == minutes, onClick = { onDailyGoalChanged(minutes) }, label = "${minutes}m")
            }
        }
        NoorToggle(checked = aiVoicePermission, onCheckedChange = onAiVoiceToggled,
            label = stringResource(Res.string.add_child_ai_voice_label),
            supportingText = stringResource(Res.string.add_child_ai_voice_desc))
    }
}

''' +s[end:]
p.write_text(s,encoding='utf-8')
p=Path('NoorHeroes/core/core-common/src/commonMain/composeResources/values/strings.xml');s=p.read_text(encoding='utf-8')
strings={'profile_multiple_children':'Have multiple children?','profile_learning_focus':'Learning Focus','profile_focus_quran':'Quran &amp; Tajweed','profile_focus_stories':'Prophet Stories','profile_focus_arabic':'Arabic Letters','profile_focus_prayers':'Salah &amp; Duas','profile_focus_values':'Islamic Values','profile_interest_science':'Science &amp; Wonders','profile_interest_arts':'Arts &amp; Crafts'}
s=s.replace('</resources>',''.join(f'    <string name="{k}">{v}</string>\n' for k,v in strings.items())+'</resources>');p.write_text(s,encoding='utf-8')
