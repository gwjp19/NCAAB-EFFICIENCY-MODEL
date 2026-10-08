# NCAAB-EFFICIENCY-MODEL

## Premiss 

Rank NCAA Basketball teams based on adjusted offensive efficiency and adjusted defensive efficiency metrics.

### Methodology 

The model calculate Points Per Possession (PPP) and Points Allowed Per Possession (PAPP) for each team on a game by game basis.

Raw efficiency metrics are then adjusted for opponent strength. 
For example, if a team scores 1.15 PPP against an opponent that typically allows only 1.05 PAPP, the team offensive performance is adjusted upward to account for the strength of the defense it faced.

The same process is applied to defensive performance using the opponent's offensive efficiency

These adjusted metrics are then used as inputs for strength of schedule adjustments, with the goal of producing opponent adjusted offensive and defensive efficiency ratings that can be used for team rankings and game simulations.

### Testing

Initial testing shows the model producing rankings that are broadly similar to established NCAA basketball rating systems such as KenPom.

Further Testing will evaluate the models predictive accuracy and determine which adjustments provide the greatest improvement.
### Future Improvements

Future additions to the rankings will include:

-Home and Away adjustments

-Weigh Recent games more than old games

-Use PPP and PAPP to create a single ranking metic (total efficiency or Points scored per points allowed)
