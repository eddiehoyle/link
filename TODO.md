## Stretch goals
- [ ] Create layout rig
- [ ] Create deform rig
- [ ] Create rig interface API
- [ ] Add more readmes


## Current issues
- [ ] Expose smarter get_control() at part level
- [ ] Expose per control grp offset functionality before build time
- [ ] Expose per control shape offset functionality after build time


## Fundamental
- [x] Split part creation so multi-parts can be made easier
- [x] Write test create methods for parts
- [ ] Write secondary (deformer) part logic
- [x] Add settings node
- [ ] Get config working
- [ ] Write data I/O logic
- [ ] Write deformer save/load data logic


## Parts
- [x] Write Fk part
- [x] Write FkChain part
- [x] Add Fk stretch logic
- [x] Write Ik part
- [x] Write Ik stretch
- [x] Add settings to proxy component
- [x] Add settings to skeleton component
- [x] Write IkFkChain part
- [x] Expose orient and point offsets to parts at creation time
- [x] Store control creation order to know first, last, etc
- [x] Add settings group
- [ ] Write a twist deformer part
- [x] Write a global part (named Base case global is reserved)
- [ ] Write spine part
- [ ] Write foot part
- [ ] Write multi part (combine parts?)
- [ ] Create face part library
- [ ] Write eye part
- [ ] Write mouth part
- [x] Write simple control part
- [ ] Create global control style to not be big quad arrow
- [ ] Aim polevector of IkRp at center of chain


## Utils
- [x] Write attribute library (properly)
- [ ] Tidy up util.name 
- [ ] Tidy up util.attr
- [ ] Add vector utils
- [x] Add joint utils for easy joint creation for test methods


## Build
- [ ] Add some more rig layout controls
