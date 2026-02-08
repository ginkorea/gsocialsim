    def step(self, num_ticks: int = 1):
        for _ in range(num_ticks):
            current_tick = self.clock.t
            all_agents = list(self.agents.agents.values())

            # --- 0. Stimulus Ingestion Phase ---
            new_stimuli_this_tick = self.stimulus_engine.tick(current_tick)
            
            # --- 1. Stimulus Perception Phase ---
            if new_stimuli_this_tick:
                for agent in all_agents:
                    for stimulus in new_stimuli_this_tick:
                        temp_content = ContentItem(
                            id=stimulus.id, author_id=stimulus.source,
                            topic=TopicId(f"stim_{stimulus.id}"), stance=0.0
                        )
                        agent.perceive(temp_content, self.world_context, stimulus_id=stimulus.id)

            # --- 2. Action Phase ---
            interactions_this_tick = []
            for agent in all_agents:
                new_interaction = agent.act(tick=current_tick)
                if new_interaction:
                    interactions_this_tick.append(new_interaction)
                    self.analytics.log_interaction(new_interaction)
            
            # --- 3. Online Interaction Perception Phase ---
            if interactions_this_tick:
                from gsocialsim.policy.bandit_learner import RewardVector
                from gsocialsim.stimuli.interaction import InteractionVerb
                
                for viewer in all_agents:
                    following_list = self.world_context.network.graph.get_following(viewer.id)
                    for interaction in interactions_this_tick:
                        if interaction.agent_id == viewer.id or interaction.agent_id not in following_list:
                            continue

                        content_to_perceive, stimulus_id, topic = None, None, None
                        
                        if interaction.verb == InteractionVerb.CREATE:
                            content_to_perceive = interaction.original_content
                            topic = content_to_perceive.topic
                        elif interaction.verb in [InteractionVerb.FORWARD, InteractionVerb.LIKE]:
                            stimulus = self.stimulus_engine.get_stimulus(interaction.target_stimulus_id)
                            if stimulus:
                                topic = TopicId(f"stim_{stimulus.id}")
                                content_to_perceive = ContentItem(id=stimulus.id, author_id=stimulus.source, topic=topic, stance=0.0)
                                stimulus_id = stimulus.id
                        
                        if content_to_perceive:
                            viewer.perceive(content_to_perceive, self.world_context, stimulus_id=stimulus_id)
                            reward = RewardVector(affiliation=0.1)
                            author = self.agents.get(interaction.agent_id)
                            if author:
                                action_key = f"{interaction.verb.value}_{topic or ''}"
                                author.learn(action_key, reward)

            day_before = self.clock.day
            self.clock.advance(1)
            if self.clock.day > day_before:
                for agent in all_agents:
                    agent.consolidate_daily(self.world_context)
